# def allow_attachment_uploader_or_inbox_staff(private_file):
#
#     print(private_file.storage)
#
#     return True


from private_storage.views import PrivateStorageView

from ticketvise.models.ticket import TicketAttachment


class TicketAttachmentDownloadView(PrivateStorageView):
    def can_access_file(self, private_file):
        return True
