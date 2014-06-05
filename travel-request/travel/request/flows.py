from viewflow import flow, lock
from viewflow.base import this, Flow

from . import views, models, tasks


class RequestFlow(Flow):
    process_cls = models.RequestApprovalProcess
    lock_impl = lock.select_for_update_lock

    # Applicant
    start = flow.Start(views.RegisterRequest) \
        .Permission(auto_create=True) \
        .Activate(this.cancel)

    cancel = flow.View(views.CancelRequest) \
        .Assign(this.start.owner) \
        .Next(this.cancelled)

    change_request = flow.View(views.ChangeRequest) \
        .Assign(this.start.owner) \
        .Next(this.approve_request)

    # Supervisor
    approve_request = flow.View(views.ApproveRequest) \
        .Permission(auto_create=True) \
        .Next(this.check_approved)

    check_approved = flow.Switch() \
        .Case(this.change_request, lambda p: p.approve_result == 'MODIFICATION') \
        .Case(this.split_actions, lambda p: p.approve_result == 'APPROVED') \
        .Case(this.rejected)

    rejected = flow.Job(tasks.send_rejection_mail) \
        .Next(this.rejected)

    # Travel agent
    split_actions = flow.Split() \
        .Next(this.book_hotel) \
        .Next(this.book_flight)

    book_hotel = flow.View(views.BookHotel) \
        .Permission(auto_create=True) \
        .Next(this.join_actions)

    book_flight = flow.View(views.BookFlight) \
        .Permission(auto_create=True) \
        .Next(this.join_actions)

    join_actions = flow.Join() \
        .Next(this.get_exchange_rate)

    get_exchange_rate = flow.Job(tasks.get_exchange_rate) \
        .Next(this.send_travel_info)

    send_travel_info = flow.Job(tasks.send_travel_info) \
        .Next(this.end)

    # End
    cancelled = flow.End()
    rejected = flow.End()
    end = flow.End()
