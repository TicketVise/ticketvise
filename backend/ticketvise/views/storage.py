from private_storage.views import PrivateStorageView


class TicketAttachmentDownloadView(PrivateStorageView):
    def can_access_file(self, private_file):
        return True
