from DatabaseTrialField import DatabaseTrialField


class SystemVar(DatabaseTrialField):

    def __init__(self):
        super().__init__()

    def get(self, matchval):
        sql = f'SELECT val FROM jkDev.SystemVar WHERE name = %(name)s'
        super.cur.execute(sql, {'name': matchval})
        row = super.cur.fetchone()

        return int(row[0])
