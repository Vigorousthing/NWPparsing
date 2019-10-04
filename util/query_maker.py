

def match_plant_subquery(eq_list):
    con_list = []
    for con in eq_list:
        con_list.append({"COMPX_ID": con})
    return {"$match": {"$or": con_list}}


















# class MongoPipelineMaker:
#     def __init__(self, initial_pipeline="[]"):
#         self.query = initial_pipeline
#
#     def add_match_stage_query(self, match_column, criteria, values):
#         if match_column == None or criteria == None or values == None:
#             return None
#         subquery = None
#         # if re.search('[^A-Za-z0-9]+', match_column) is not None or re.search('[^A-Za-z0-9]+', values) is not None :
#         #     raise TypeError
#         if criteria == "equal":
#             subquery = "{%s: '%s'}" % (match_column, values)
#         elif criteria == "greater":
#             subquery = "{%s: {$gt: '%s'}}" % (match_column, values)
#         elif criteria == "less":
#             subquery = "{%s: {$lt: '%s'}}" % (match_column, values)
#         elif criteria == "interval":
#             subquery = "{%s: {$gte: '%s', $lt: '%s'}}" % (match_column, values[0], values[1])
#         elif criteria == "or":
#             or_paragraph = ""
#             for value in values:
#                 if type(value) == str:
#                     or_paragraph = or_paragraph + "{%s: '%s'}" % (match_column, value) + ","
#                 else:
#                     or_paragraph = or_paragraph + "{%s: %s}" % (match_column, value) + ","
#             subquery = "{$or : [%s]}" % or_paragraph
#         elif criteria == "exclude":
#             nor_paragraph = ""
#             for value in values:
#                 if type(value) == str:
#                     nor_paragraph = nor_paragraph + "{%s: '%s'}" % (match_column, value) + ","
#                 else:
#                     nor_paragraph = nor_paragraph + "{%s: %s}" % (match_column, value) + ","
#             subquery = "{$nor : [%s]}" % nor_paragraph
#
#         stage_query = "{$match: %s}" % subquery
#         if len(self.query[1:-1]) == 0:
#             self.query = "[" + stage_query + "]"
#         else:
#             self.query = "[" + self.query[1:-1] + ", " + stage_query + "]"
#
#     def add_simple_project_query(self, project_list):
#
#         # for col in project_list:
#         #     if re.search('[^A-Za-z0-9]+', col) is not None:
#         #         raise TypeError
#
#         project_list_dic = {}
#         for col in project_list:
#             project_list_dic[col] = 1
#         subquery = str(project_list_dic)
#         stage_query = "{$project: %s}" % subquery
#         self.query = "[" + self.query[1:-1] + ", " + stage_query + "]"