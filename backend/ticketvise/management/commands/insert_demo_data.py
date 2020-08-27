import datetime

from django.core.management import BaseCommand
from django.db import IntegrityError, transaction
from django.utils import timezone

from ticketvise.models.comment import Comment
from ticketvise.models.inbox import Inbox
from ticketvise.models.label import Label
from ticketvise.models.ticket import Ticket, Status
from ticketvise.models.user import User, UserInbox, Role


class Command(BaseCommand):
    """Django command that insert demo data into the database."""

    def handle(self, *args, **options):
        """Handle the command"""
        try:
            self.insert_data()
            print("Successfully populated database with demo data!")
        except IntegrityError as e:
            print("Database seems already populated with demo data, IntegrityError: ", e)

    @transaction.atomic
    def insert_data(self):
        # Creating users, default password = "admin193"
        password = "pbkdf2_sha256$180000$6zy2oz9vnxsr$eTQBZxgVxG7ldORL63+OcqJbzLcUhbdCkAW7NdqsOxE="
        user_admin = User.objects.create(
            username="admin",
            first_name="admin",
            last_name="admin",
            password=password,
            email="admin@ticketvise.com",
            is_staff=True,
            is_superuser=True,
        )
        user_ivan = User.objects.create(
            username="ivanstudent",
            first_name="Ivan",
            last_name="Student",
            password=password,
            email="ivanstudent@ticketvise.com",
            is_staff=False,
            is_superuser=False,
        )
        user_julian = User.objects.create(
            username="julianstudent",
            first_name="Julian",
            last_name="Student",
            password=password,
            email="julianstudent@ticketvise.com",
            is_staff=False,
            is_superuser=False,
        )
        user_jelle = User.objects.create(
            username="jelleassistant",
            first_name="Jelle",
            last_name="Assistant",
            password=password,
            email="jelleassistant@ticketvise.com",
            is_staff=True,
            is_superuser=True,
        )
        user_ana = User.objects.create(
            username="anacoordinator",
            first_name="Ana",
            last_name="Coordinator",
            password=password,
            email="anacoordinator@ticketvise.com",
            is_staff=True,
            is_superuser=True,
        )
        user_bryan = User.objects.create(
            username="bryanstudent",
            first_name="Bryan",
            last_name="Student",
            password=password,
            email="bryanstudent@ticketvise.com",
            is_staff=True,
            is_superuser=True,
        )
        user_tom = User.objects.create(
            username="tomassistant",
            first_name="Tom",
            last_name="Assistant",
            password=password,
            email="tomassistant@ticketvise.com",
            is_staff=True,
            is_superuser=True,
        )
        user_marco = User.objects.create(
            username="marcoassistant",
            first_name="Marco",
            last_name="Assistant",
            password=password,
            email="marcoassistant@ticketvise.com",
            is_staff=True,
            is_superuser=True,
        )
        user_no_pass = User.objects.create(
            username="nopass", first_name="no", last_name="password", email="nopass@ticketvise.com"
        )

        # Creating Courses
        inbox_pse = Inbox.objects.create(
            code="5062STRE6Y", name="Project Software Engineering", color="#2ad43b", round_robin_parameter=4
        )
        inbox_ip = Inbox.objects.create(code="5062BEST6Y", name="Inleiding Programmeren", color="#45b6fe")
        inbox_ds = Inbox.objects.create(code="5061DAVI6Y", name="Datastructuren", color="#7cfc00")

        inbox_pt = Inbox.objects.create(code="5061DAVI5Y", name="Programmeertalen", color="#ff1717")
        inbox_mp = Inbox.objects.create(code="5061GAVI5Y", name="Master's Project ", color="#30139c")
        inbox_pmpse = Inbox.objects.create(
            code="5061VEVI5Y", name="Preparation Master's Project Software Engineering ", color="#138e9c"
        )

        # Creating Labels
        label_ds_heaps = Label.objects.create(inbox=inbox_ds, name="Heaps", color="#ff0000", is_visible_to_guest=True)
        label_ds_list = Label.objects.create(inbox=inbox_ds, name="Linked List", color="#0097ff",
                                             is_visible_to_guest=True)
        label_ds_hash = Label.objects.create(inbox=inbox_ds, name="Hash Table", color="#0ec81d",
                                             is_visible_to_guest=True)
        label_pse_swebok = Label.objects.create(
            inbox=inbox_pse,
            name="SWEBOK",
            color="#ff0000",
        )
        label_pse_report = Label.objects.create(
            inbox=inbox_pse,
            name="Individual Report",
            color="#29ff00",
            is_visible_to_guest=True,
        )
        label_pse_lecture = Label.objects.create(
            inbox=inbox_pse,
            name="Lecture",
            color="#0090ff",
            is_visible_to_guest=True,
        )
        label_pse_ejournal = Label.objects.create(inbox=inbox_pse, name="E-Journal", color="#fbf06d",
                                                  is_visible_to_guest=True)
        label_pse_laptop = Label.objects.create(inbox=inbox_pse, name="Laptop", color="#150a1a",
                                                is_visible_to_guest=True)
        label_pse_assignment = Label.objects.create(inbox=inbox_pse, name="Assignment", color="#00ffcd",
                                                    is_visible_to_guest=True)
        label_ip_hotel = Label.objects.create(inbox=inbox_ip, name="Hotel", color="#00b5fe", is_visible_to_guest=True)
        label_ip_quack = Label.objects.create(
            inbox=inbox_ip,
            name="Dr. Quackerjack",
            color="#ff0000",
            is_visible_to_guest=True,
        )

        # Creating user-inbox relationships
        # UserInbox.objects.create(user=user_admin, role=Role.AGENT)
        # UserInbox.objects.create(user=user_admin, role=Role.GUEST)
        UserInbox.objects.create(user=user_ivan, role=Role.GUEST, inbox=inbox_ds)
        UserInbox.objects.create(user=user_ivan, role=Role.GUEST, inbox=inbox_ip)
        UserInbox.objects.create(user=user_ivan, role=Role.GUEST, inbox=inbox_pse)
        UserInbox.objects.create(user=user_julian, role=Role.GUEST, inbox=inbox_pse)
        UserInbox.objects.create(user=user_jelle, role=Role.AGENT, inbox=inbox_ds)
        UserInbox.objects.create(user=user_jelle, role=Role.AGENT, inbox=inbox_ip)
        UserInbox.objects.create(user=user_jelle, role=Role.AGENT, inbox=inbox_pse)
        UserInbox.objects.create(user=user_ana, role=Role.MANAGER, inbox=inbox_pse)
        UserInbox.objects.create(user=user_ana, role=Role.MANAGER, inbox=inbox_pt)
        UserInbox.objects.create(user=user_ana, role=Role.MANAGER, inbox=inbox_mp)
        UserInbox.objects.create(user=user_ana, role=Role.MANAGER, inbox=inbox_pmpse)
        UserInbox.objects.create(user=user_bryan, role=Role.AGENT, inbox=inbox_ds)
        UserInbox.objects.create(user=user_bryan, role=Role.AGENT, inbox=inbox_ip)
        UserInbox.objects.create(user=user_bryan, role=Role.GUEST, inbox=inbox_pse)
        UserInbox.objects.create(user=user_tom, role=Role.AGENT, inbox=inbox_pse)
        UserInbox.objects.create(user=user_tom, role=Role.AGENT, inbox=inbox_ds)
        UserInbox.objects.create(user=user_tom, role=Role.AGENT, inbox=inbox_ip)
        UserInbox.objects.create(user=user_marco, role=Role.AGENT, inbox=inbox_pse)
        UserInbox.objects.create(user=user_marco, role=Role.AGENT, inbox=inbox_ds)
        UserInbox.objects.create(user=user_marco, role=Role.AGENT, inbox=inbox_ip)

        # Creating tickets
        ticket_10 = Ticket.objects.create(
            author=user_bryan,
            assignee=user_ana,
            inbox=inbox_pse,
            title="What should the length of the individual report be?",
            content="I started working on the indivual report in the last few days. However, it\
        is not completely clear to me what the length of this report should be. Could anyone give me some further insight into\
        this?",
        )
        ticket_10.date_created = timezone.now() - datetime.timedelta(days=2, hours=19)
        ticket_10.date_edited = timezone.now() - datetime.timedelta(days=2, hours=19)
        ticket_10.add_label(label_pse_report)
        ticket_10.status = Status.ANSWERED
        ticket_10.save()

        ticket_11 = Ticket.objects.create(
            author=user_bryan,
            assignee=user_jelle,
            inbox=inbox_pse,
            title="Do we have to read SWEBOK completely?",
            content="The book is very long and I think it is a dry read. Do we need to read the complete\
        book, or simply a part of the chapters?",
        )
        ticket_11.date_created = timezone.now() - datetime.timedelta(days=5, hours=2)
        ticket_11.date_edited = timezone.now() - datetime.timedelta(days=5, hours=2)
        ticket_11.add_label(label_pse_swebok)
        ticket_11.status = Status.ANSWERED
        ticket_11.save()

        ticket_12 = Ticket.objects.create(
            author=user_ivan,
            inbox=inbox_ip,
            title="Dr. Quackerjack gnome sort already works",
            content="The gnome sort function already completely works, whilst I have not changed a single\
        line in that function. Can I leave the function as it is, or do I need to rewrite it myself?",
        )
        ticket_12.add_label(label_ip_quack)
        ticket_12.status = ticket_12.assign_to(user_jelle)

        ticket_13 = Ticket.objects.create(
            author=user_ivan,
            inbox=inbox_ip,
            title="How many rooms does the hotel have?",
            content="I don't understand how many rooms the hotel should have..",
        )
        ticket_13.add_label(label_ip_hotel)

        ticket_14 = Ticket.objects.create(
            author=user_ivan,
            inbox=inbox_ds,
            title="Do we need to make a singly linked list or a doubly linked list?",
            content="From the lecture I understood that getting the previous element in a doubly linked\
        list is in O(1) instead of O(n). However, the other functions may become slower cause I\
        need to change more pointers. So what type of list do I need to implement?",
        )
        ticket_14.add_label(label_ds_list)

        ticket_15 = Ticket.objects.create(
            author=user_ivan,
            inbox=inbox_ds,
            title="What's the difference between a hash table and a linked list?",
            status=Status.ANSWERED,
            content="Both seem to use a linked list..",
        )
        ticket_15.add_label(label_ds_list)
        ticket_15.add_label(label_ds_hash)

        ticket_16 = Ticket.objects.create(
            author=user_ivan,
            inbox=inbox_pse,
            assignee=user_ana,
            title="When is the next SWEBOK panel?",
            content="On Canvas the times do not indicate the group.",
            status=Status.ASSIGNED,
        )
        ticket_16.add_label(label_pse_swebok)

        ticket_17 = Ticket.objects.create(
            author=user_ivan,
            inbox=inbox_pse,
            assignee=user_tom,
            title="E-Journal does not work",
            content="E-Journal does not work",
        )
        ticket_17.add_label(label_pse_ejournal)
        ticket_17.status = Status.CLOSED
        ticket_17.date_created = timezone.now() - datetime.timedelta(days=18, hours=2)
        ticket_17.date_edited = timezone.now() - datetime.timedelta(days=18, hours=2)
        ticket_17.save()

        ticket_18 = Ticket.objects.create(
            author=user_bryan,
            assignee=user_marco,
            inbox=inbox_pse,
            title="Are there any assignments for this inbox?",
            content="Are there any assignments for this inbox?",
        )
        ticket_18.date_created = timezone.now() - datetime.timedelta(days=4, hours=1)
        ticket_18.date_edited = timezone.now() - datetime.timedelta(days=4, hours=1)
        ticket_18.add_label(label_pse_assignment)
        ticket_18.status = Status.ANSWERED
        ticket_18.save()

        ticket_19 = Ticket.objects.create(
            author=user_ivan,
            assignee=user_tom,
            inbox=inbox_pse,
            title="My laptop broke.",
            content="I cannot help my team or make my report, help!",
        )
        ticket_19.date_created = timezone.now() - datetime.timedelta(hours=23)
        ticket_19.date_edited = timezone.now() - datetime.timedelta(hours=23)
        ticket_19.add_label(label_pse_laptop)
        ticket_19.add_label(label_pse_report)
        ticket_19.status = Status.ANSWERED
        ticket_19.save()

        ticket_20 = Ticket.objects.create(
            author=user_ivan,
            assignee=user_tom,
            inbox=inbox_pse,
            title="What should be the content of the demo?",
            content="What should be the content of the demo?",
        )
        ticket_20.date_created = timezone.now() - datetime.timedelta(days=9, hours=23)
        ticket_20.date_edited = timezone.now() - datetime.timedelta(days=9, hours=23)
        ticket_20.add_label(label_pse_lecture)
        ticket_20.status = Status.ANSWERED
        ticket_20.save()

        ticket_21 = Ticket.objects.create(
            author=user_ivan,
            assignee=user_jelle,
            inbox=inbox_pse,
            title="Discord does not work on my laptop!",
            content="Discord does not work on my laptop!",
        )
        ticket_21.date_created = timezone.now() - datetime.timedelta(days=3)
        ticket_21.date_edited = timezone.now() - datetime.timedelta(days=3)
        ticket_21.add_label(label_pse_laptop)
        ticket_21.status = Status.ANSWERED
        ticket_21.save()

        ticket_22 = Ticket.objects.create(
            author=user_bryan,
            assignee=user_jelle,
            inbox=inbox_pse,
            title="Was eJournal founded during this inbox?",
            content="Was eJournal founded during this inbox?",
        )
        ticket_22.date_created = timezone.now() - datetime.timedelta(days=1, hours=17)
        ticket_22.date_edited = timezone.now() - datetime.timedelta(days=1, hours=17)
        ticket_22.add_label(label_pse_ejournal)
        ticket_22.status = Status.ANSWERED
        ticket_22.save()

        ticket_23 = Ticket.objects.create(
            author=user_bryan,
            inbox=inbox_pse,
            assignee=user_ana,
            title="Is there a lecture on the day of the demo?",
            content="Is there a lecture on the day of the demo? I want to make my report!",
            status=Status.ASSIGNED,
        )
        ticket_23.date_created = timezone.now() - datetime.timedelta(hours=2)
        ticket_23.date_edited = timezone.now() - datetime.timedelta(hours=2)
        ticket_23.add_label(label_pse_lecture)
        ticket_23.add_label(label_pse_report)
        ticket_23.save()

        ticket_24 = Ticket.objects.create(
            author=user_bryan,
            inbox=inbox_pse,
            assignee=user_tom,
            title="Why are there no project proposals for eJournal?",
            content="Why are there no project proposals for eJournal?",
            status=Status.ASSIGNED,
        )
        ticket_24.date_created = timezone.now() - datetime.timedelta(hours=1, minutes=23)
        ticket_24.date_edited = timezone.now() - datetime.timedelta(hours=1, minutes=23)
        ticket_24.add_label(label_pse_assignment)
        ticket_24.add_label(label_pse_ejournal)
        ticket_24.save()

        ticket_25 = Ticket.objects.create(
            author=user_bryan,
            inbox=inbox_pse,
            assignee=user_jelle,
            title="Should the SWEBOK panel questions I answered in " + "eJournal be in my individual report?",
            content="Should the SWEBOK panel questions I answered in " + "eJournal be in my individual report?",
            status=Status.ASSIGNED,
        )
        ticket_25.date_created = timezone.now() - datetime.timedelta(minutes=43)
        ticket_25.date_edited = timezone.now() - datetime.timedelta(minutes=43)
        ticket_25.add_label(label_pse_swebok)
        ticket_25.add_label(label_pse_report)
        ticket_25.add_label(label_pse_ejournal)
        ticket_25.save()

        ticket_26 = Ticket.objects.create(
            author=user_ivan,
            inbox=inbox_pse,
            assignee=user_ana,
            title="Is there a minimum grade for my individual report?",
            content="Is there a minimum grade for my individual report?",
        )
        ticket_26.add_label(label_pse_report)
        ticket_26.add_label(label_pse_assignment)
        ticket_26.status = Status.CLOSED
        ticket_26.date_created = timezone.now() - datetime.timedelta(days=28, hours=17)
        ticket_26.date_edited = timezone.now() - datetime.timedelta(days=28, hours=17)
        ticket_26.save()

        ticket_27 = Ticket.objects.create(
            author=user_ivan,
            inbox=inbox_pse,
            assignee=user_jelle,
            title="Where can I find the SWEBOK?",
            content="Where can I find the SWEBOK?",
        )
        ticket_27.add_label(label_pse_swebok)
        ticket_27.status = Status.CLOSED
        ticket_27.date_created = timezone.now() - datetime.timedelta(days=23, hours=13)
        ticket_27.date_edited = timezone.now() - datetime.timedelta(days=23, hours=13)
        ticket_27.save()

        ticket_28 = Ticket.objects.create(
            author=user_bryan,
            inbox=inbox_pse,
            assignee=user_jelle,
            title="Do we have to make any smaller assignments?",
            content="Do we have to make any smaller assignments?",
        )
        ticket_28.add_label(label_pse_assignment)
        ticket_28.status = Status.CLOSED
        ticket_28.date_created = timezone.now() - datetime.timedelta(days=15, hours=3)
        ticket_28.date_edited = timezone.now() - datetime.timedelta(days=15, hours=3)
        ticket_28.save()

        ticket_29 = Ticket.objects.create(
            author=user_bryan,
            inbox=inbox_pse,
            assignee=user_marco,
            title="Which parts of SWEBOK do we have to read?",
            content="Which parts of SWEBOK do we have to read?",
        )
        ticket_29.add_label(label_pse_swebok)
        ticket_29.status = Status.CLOSED
        ticket_29.date_created = timezone.now() - datetime.timedelta(days=18, hours=21)
        ticket_29.date_edited = timezone.now() - datetime.timedelta(days=18, hours=21)
        ticket_29.save()

        ticket_30 = Ticket.objects.create(
            author=user_bryan,
            inbox=inbox_pse,
            assignee=user_ana,
            title="Should we write the individual report in the passive form?",
            content="Should we write the individual report in the passive form?",
        )
        ticket_30.add_label(label_pse_report)
        ticket_30.add_label(label_pse_assignment)
        ticket_30.status = Status.CLOSED
        ticket_30.date_created = timezone.now() - datetime.timedelta(days=11, hours=15)
        ticket_30.date_edited = timezone.now() - datetime.timedelta(days=11, hours=15)
        ticket_30.save()

        ticket_31 = Ticket.objects.create(
            author=user_bryan, inbox=inbox_pse, title="How long should the demo be?",
            content="How long should the demo be?",
        )
        ticket_31.add_label(label_pse_assignment)
        ticket_31.status = Status.PENDING
        ticket_31.date_created = timezone.now() - datetime.timedelta(minutes=5)
        ticket_31.date_edited = timezone.now() - datetime.timedelta(minutes=5)
        ticket_31.save()

        ticket_32 = Ticket.objects.create(
            author=user_ivan,
            inbox=inbox_pse,
            title="Should I mention the testing coverage in my report?",
            content="Should I mention the testing coverage in my report?",
        )
        ticket_32.add_label(label_pse_assignment)
        ticket_32.add_label(label_pse_report)
        ticket_32.status = Status.CLOSED
        ticket_32.date_created = timezone.now() - datetime.timedelta(days=18, hours=2)
        ticket_32.date_edited = timezone.now() - datetime.timedelta(days=18, hours=2)
        ticket_32.save()

        ticket_33 = Ticket.objects.create(
            author=user_julian,
            inbox=inbox_pse,
            assignee=user_ana,
            title="I found a security leak in eJournal!",
            content="They are susceptible to DDoSing, do you guys have the contact\
        details of the developers so I can tell them?",
        )
        ticket_33.add_label(label_pse_ejournal)
        ticket_33.status = Status.CLOSED
        ticket_33.date_created = timezone.now() - datetime.timedelta(days=18, hours=5)
        ticket_33.date_edited = timezone.now() - datetime.timedelta(days=18, hours=5)
        ticket_33.save()

        ticket_34 = Ticket.objects.create(
            author=user_ivan,
            inbox=inbox_pse,
            assignee=user_ana,
            title="The SWEBOK panel dates do not specify the group",
            content="The SWEBOK panel dates do not specify the group",
        )
        ticket_34.add_label(label_pse_swebok)
        ticket_34.status = Status.CLOSED
        ticket_34.date_created = timezone.now() - datetime.timedelta(days=28, hours=16)
        ticket_34.date_edited = timezone.now() - datetime.timedelta(days=28, hours=16)
        ticket_34.save()

        ticket_35 = Ticket.objects.create(
            author=user_julian,
            inbox=inbox_pse,
            assignee=user_ana,
            title="Are the lectures mandatory?",
            content="I have to join a lecture of an extracurricular " + "inbox I am taking at the same time.",
        )
        ticket_35.add_label(label_pse_lecture)
        ticket_35.status = Status.CLOSED
        ticket_35.date_created = timezone.now() - datetime.timedelta(days=28, hours=15)
        ticket_35.date_edited = timezone.now() - datetime.timedelta(days=28, hours=15)
        ticket_35.save()

        ticket_36 = Ticket.objects.create(
            author=user_bryan,
            assignee=user_ana,
            inbox=inbox_pse,
            title="Are the SWEBOK panels related to the book or the papers?",
            content="Are the SWEBOK panels related to the book or the papers?",
        )
        ticket_36.date_created = timezone.now() - datetime.timedelta(days=2, hours=18)
        ticket_36.date_edited = timezone.now() - datetime.timedelta(days=2, hours=18)
        ticket_36.add_label(label_pse_swebok)
        ticket_36.status = Status.ANSWERED
        ticket_36.save()

        # Create Comments
        def add_date_to_comment(comment: Comment, timedelta):
            """
            Add the creation and editted date to the comment object.
            """
            comment.date_created = timezone.now() - timedelta
            comment.date_edited = timezone.now() - timedelta
            comment.save()

        comment_11 = Comment.objects.create(
            author=user_jelle,
            ticket=ticket_11,
            is_reply=True,
            content="You only have to read the chapters that are linked to the papers",
        )
        add_date_to_comment(comment_11, datetime.timedelta(days=5, hours=1))

        Comment.objects.create(
            author=user_jelle,
            ticket=ticket_15,
            is_reply=True,
            content="Good question! The linked list in the hash table is simply used to handle\
        collisions when the hash functions gives the same hash index to two different entries.",
        )

        comment_10 = Comment.objects.create(
            author=user_ana, ticket=ticket_10, is_reply=True, content="2 pages, however this is not a hard limit.",
        )
        add_date_to_comment(comment_10, datetime.timedelta(days=2, hours=14))
        comment_10 = Comment.objects.create(
            author=user_jelle, ticket=ticket_10, is_reply=True, content="I recommend 3 pages.",
        )
        add_date_to_comment(comment_10, datetime.timedelta(days=2, hours=15))

        comment_17 = Comment.objects.create(
            author=user_tom, ticket=ticket_17, is_reply=True, content="It should be working again!",
        )
        add_date_to_comment(comment_17, datetime.timedelta(days=18, hours=2))

        comment_18 = Comment.objects.create(
            author=user_marco, ticket=ticket_18, is_reply=True, content="Yes, you need to write an individual report.",
        )
        add_date_to_comment(comment_18, datetime.timedelta(days=3, hours=14))

        comment_19 = Comment.objects.create(
            author=user_tom, ticket=ticket_19, is_reply=True,
            content="Maybe you can borrow a laptop from one of your peers.",
        )
        add_date_to_comment(comment_19, datetime.timedelta(hours=13))

        comment_20 = Comment.objects.create(
            author=user_tom, ticket=ticket_20, is_reply=True, content="All the killer features, of inbox.",
        )
        add_date_to_comment(comment_20, datetime.timedelta(days=9, hours=2))

        comment_21 = Comment.objects.create(author=user_jelle, ticket=ticket_21, is_reply=True, content="Unlucky.", )
        add_date_to_comment(comment_21, datetime.timedelta(days=2, hours=14))

        comment_22 = Comment.objects.create(author=user_jelle, ticket=ticket_22, is_reply=True,
                                            content="Yes! Cool, right?", )
        add_date_to_comment(comment_22, datetime.timedelta(days=1, hours=15))

        comment_26 = Comment.objects.create(author=user_ana, ticket=ticket_26, is_reply=True, content="No.", )
        add_date_to_comment(comment_26, datetime.timedelta(days=28, hours=6))

        comment_30 = Comment.objects.create(
            author=user_ana, ticket=ticket_30, is_reply=True, content="Yes, you should for a better grade.",
        )
        add_date_to_comment(comment_30, datetime.timedelta(days=11, hours=1))

        comment_32 = Comment.objects.create(
            author=user_ana, ticket=ticket_32, is_reply=True, content="You could do that, as it would be interesting.",
        )
        add_date_to_comment(comment_32, datetime.timedelta(days=18, hours=1))

        comment_33 = Comment.objects.create(
            author=user_ana,
            ticket=ticket_33,
            is_reply=True,
            content="Seems scary... Please contact Lars, Maarten and Engel about this.",
        )
        add_date_to_comment(comment_33, datetime.timedelta(days=18, hours=1))

        comment_34 = Comment.objects.create(author=user_ana, ticket=ticket_34, is_reply=True,
                                            content="Should be fixed now", )
        add_date_to_comment(comment_34, datetime.timedelta(days=28, hours=13))

        comment_35 = Comment.objects.create(
            author=user_ana, ticket=ticket_35, is_reply=True,
            content="No, but it is highly recommended to join them...",
        )
        add_date_to_comment(comment_35, datetime.timedelta(days=28, hours=13))

        comment_36 = Comment.objects.create(author=user_ana, ticket=ticket_36, is_reply=True,
                                            content="Only the papers!", )
        add_date_to_comment(comment_36, datetime.timedelta(days=2, hours=14))
