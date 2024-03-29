

class Query:
    def __init__(self, table):
        self.table = table
        self.fields = []
        self._group = []
        self.wheres = []
        self.order = {}
        self.joins = []
        self.queryjoins = []

    def where(self, condition):
        if isinstance(condition, list):
            self.wheres.extend(condition)
        else:
            self.wheres.append(condition)

    def queryjoin(self, query, query_name, join_field, query_field):
        self.joins.append("({}) {}".format(query.get(), query_name))
        self.wheres.append("{}.{} = {}.{}".format(self.table, join_field, query_name, query_field))

    # Medio hack, solo vamos a poder hacer join entre dos tablas
    # TODO quizas ver de extender esto
    # Dejo joins como vector por si eventualmente hacemos multiple joins
    def join(self, other_table, join_field, other_join_field):
        self.joins.append(other_table)
        self.wheres.append("{}.{} = {}.{}".format(self.table, join_field, other_table, other_join_field))
    
    def select(self, field):
        if isinstance(field, list):
            self.fields.extend(field)
        else:
            self.fields.append(field)

    def group_by(self, field):
        if isinstance(field, list):
            self._group.extend(field)
        else:
            self._group.append(field)

    def orderby(self, field, value):
        self.order[field] = value

    def get(self):
        query = []

        # SELECT 
        query.append("SELECT ")
        if len(self.fields) > 0:
            query.append(', '.join(self.fields))
        else:
            query.append('*')
        # FROM
        query.append(" FROM {}".format(self.table))
        if len(self.joins) > 0:
            for join in self.joins:
                query.append(", {} ".format(join))

        # WHERE
        if len(self.wheres) > 0:
            query.append(" WHERE (")
            i = 0
            for cond in self.wheres:
                if i != 0:
                    query.append(" AND ")
                query.append("{}".format(cond))
                i+= 1
            query.append(")")
        # GROUP
        if len(self._group) > 0:
            query.append(" GROUP BY  ")
            i = 0
            for group in self._group:
                if i != 0:
                    query.append(", ")
                query.append(" {}".format(group))
                i+= 1
        # ORDER
        if len(self.order) > 0:
            query.append(" ORDER BY ")
            i = 0
            for k in self.order.keys():
                if i != 0:
                    query.append(", ")
                query.append(" {} {}".format(k, self.order[k]))
                i+= 1
        return ''.join(query)