import ftplib
import CONSTANT
import os
from util.Visualizer import Visualizer
from util.input_converter import InputConverter


class FtpAccessor:
    def __init__(self, ip, id, pw):
        self.ip = ip
        self.id = id
        self.pw = pw

        self.ftp = ftplib.FTP()

        # how to check connection
        self.ftp.connect(ip)
        self.ftp.login(id, pw)

        self.visualizer = Visualizer()
        self.converter = InputConverter()

    def download_files(self, filename_list, file_type):
        self.ftp.cwd(CONSTANT.ftp_ROOT + file_type)

        for i, filename in enumerate(filename_list):
            path = os.path.join(CONSTANT.download_path, filename)
            if os.path.exists(path):
                print(CONSTANT.already_exists_text.format(filename))
                continue
            else:
                try:
                    new_file = open(path, "wb")
                    self.ftp.retrbinary("RETR " + filename, new_file.write)
                    new_file.close()
                except ftplib.error_perm:
                    os.remove(path)
                    # new_file.close()
                    print(CONSTANT.download_exception_text.format(filename))
            self.visualizer.print_progress(i, len(filename_list),
                                           "Download Progress: ", "Complete",
                                           1, 50)
        self.ftp.close()

    # def existence_check(self, file_type, fold_type, horizon, crtn_tm):
    #     self.converter.current_time_conversion(crtn_tm)
    #     name = "{}_{}_h{}.{}.gb2".format()
    #
    #     not_found_list = []
    #
    #     return not_found_list

    def existence_check(self, filename):
        try:
            self.ftp.sendcmd("MLST /LDAPS/" + filename)
            return True
        except ftplib.error_perm:
            return False

    def reconnect(self):
        self.ftp.connect(self.ip)
        self.ftp.login(self.id, self.pw)

    def check_connection(self):
        try:
            self.ftp.voidcmd("NOOP")
        except AttributeError:
            return False
        else:
            return True

    def size_check(self, filename_list, file_type):
        self.ftp.cwd(CONSTANT.ftp_ROOT + file_type)

        file_size = 0
        file_num = 0
        for file_name in filename_list:
            path = os.path.join(CONSTANT.local_path, file_name)
            if not os.path.exists(path):
                try:
                    file_size += self.ftp.size(file_name)
                    file_num += 1
                except ftplib.error_perm:
                    print(file_name + " not exists in ftp server")
        print("total size of files : ", float(file_size) / (1024 * 1024 * 1024)
              , "gb", ", total number of files :",
              file_num)

    def remove_from_local_pc(self, filename_list):
        for filename in filename_list:
            path = os.path.join(CONSTANT.local_path, filename)
            if os.path.exists(path):
                os.remove(path)
            else:
                print("cannot remove " + filename +
                      " because the file does not exists in local pc")

    def close(self):
        self.ftp.close()
