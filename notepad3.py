from controllers.eval_maker import *


time_interval = [2019100106, 2019100406]

eval_maker = JenonEval(time_interval)
# eval_maker.create_data_and_merge()
# eval_maker.make_checkpoint("jenoncheckpoint.xlsx")
eval_maker.load_checkpoint("jenoncheckpoint.xlsx")

eval_maker.merged = eval_maker.merged.dropna()
# print(eval_maker.merged)
# print(eval_maker.merged.dropna().to_excel(
#     CONSTANT.data_file_path+"dropnatest0107.xlsx"))
#
eval_maker.make_criteria_column_and_groupby_horizon()
eval_maker.cal_final_criteria()
eval_maker.save_output("jenontest0106.xlsx")

