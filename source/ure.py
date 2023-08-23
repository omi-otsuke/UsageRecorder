import datetime


class UsageRecordEntity:
    def __init__(
        self,
        begin_datetime: datetime.datetime = datetime.datetime(1, 1, 1, 0, 0, 0),
        end_datetime: datetime.datetime = datetime.datetime(1, 1, 1, 0, 0, 0),
        user_name: str = "",
        connection_account: str = "",
        use_purpose: str = "",
        server_names: list = [],
        remarks: str = "",
        update_date: datetime.date = datetime.date(1, 1, 1),
    ):
        self.begin_datetime = begin_datetime
        self.end_datetime = end_datetime
        self.user_name = user_name
        self.connection_account = connection_account
        self.use_purpose = use_purpose
        self.server_names = server_names
        self.remarks = remarks
        self.update_date = update_date
