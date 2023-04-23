import tkinter as tk
import datetime
import pyodbc
from tkinter import messagebox

class SinhVien:
    def __init__(self):
        self.__ma_sv = None
        self.__ho_ten = None
        self.__gioi_tinh = None
        self.__ngay_sinh = None
        self.__lop = None

    def ma_sv_set(self, ma_sv):
        self.ma_sv = ma_sv
    def hoten_set(self):
    def gioi_tinh_set(self):
    def ngay_sinh_set(self):
    def lop_set(self):

    def masv_get(self, ma_sv):
        return self.ma_sv
    def ho_ten_get(self):
    def gioi_tinh_get(self):
    def ngay_sinh_get(self):
    def lop_get(self):


class MonHoc:

class GiaoVien:


class QuanLiSinhVien():
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Quản Lý Sinh Viên")
        self.window.geometry("1250x700+150+50")
        self.create_gui()

        sv = 'DESKTOP-GTIDRT8'
        dbs = 'QLSV'
        usr = 'sa'
        pwd = 'sa'
        dbs = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + sv + ';DATABASE=' + dbs + ';UID=' + usr + ';PWD=' + pwd + ';autocommit=True')
        self.cursor = dbs.cursor()

    def create_gui(self):
        # Tạo các đối tượng GUI
        self.lbl_ma_sv = tk.Label(self.window, text="Mã SV:")
        self.lbl_ma_sv.grid(row=17, column=30, padx=5, pady=5)
        self.txt_ma_sv = tk.Entry(self.window)
        self.txt_ma_sv.grid(row=17, column=31,   padx=5, pady=5)

        self.lbl_ho_ten = tk.Label(self.window, text="Họ Tên:")
        self.lbl_ho_ten.grid(row=18, column=30, padx=5, pady=5)
        self.txt_ho_ten = tk.Entry(self.window)
        self.txt_ho_ten.grid(row=18, column=31, padx=5, pady=5)

        self.lbl_gioi_tinh = tk.Label(self.window, text="Giới Tính:")
        self.lbl_gioi_tinh.grid(row=19, column=30, padx=5, pady=5)
        self.txt_gioi_tinh = tk.Entry(self.window)
        self.txt_gioi_tinh.grid(row=19, column=31, padx=5, pady=5)

        self.lbl_ngay_sinh = tk.Label(self.window, text="Ngày Sinh:")
        self.lbl_ngay_sinh.grid(row=20, column=30, padx=5, pady=5)
        self.txt_ngay_sinh = tk.Entry(self.window)
        self.txt_ngay_sinh.grid(row=20, column=31, padx=5, pady=5)

        self.lbl_lop = tk.Label(self.window, text="Lớp:")
        self.lbl_lop.grid(row=21, column=30, padx=5, pady=5)
        self.txt_lop = tk.Entry(self.window)
        self.txt_lop.grid(row=21, column=31, padx=5, pady=5)

        self.btn_them = tk.Button(self.window, text="Thêm", command=self.them_sinh_vien)
        self.btn_them.grid(row=22, column=31, padx=5, pady=5)

        self.btn_xem = tk.Button(self.window, text="Xem", command=self.xem_sinh_vien)
        self.btn_xem.grid(row=22, column=32, padx=5, pady=5)

        self.btn_cap_nhat = tk.Button(self.window, text="Cập Nhật", command=self.cap_nhat_sinh_vien)
        self.btn_cap_nhat.grid(row=23, column=31, padx=5, pady=5)
        self.btn_xoa = tk.Button(self.window, text="Xóa", command=self.xoa_sinh_vien)
        self.btn_xoa.grid(row=23, column=32, padx=5, pady=5)

        self.lbl_ket_qua = tk.Label(self.window, text="")
        self.lbl_ket_qua.grid(row=7, columnspan=2, padx=5, pady=5)
    def clear_input(self):
        # Xóa dữ liệu trên các ô nhập liệu
        self.txt_ma_sv.delete(0, tk.END)
        self.txt_ho_ten.delete(0, tk.END)
        self.txt_gioi_tinh.delete(0, tk.END)
        self.txt_ngay_sinh.delete(0, tk.END)
        self.txt_lop.delete(0, tk.END)
    def run(self):
        # Chạy giao diện chính
        self.window.mainloop()

    def xem_sv(self):
        # Hiển thị danh sách sinh viên trong MessageBox
        danh_sach = "Danh sách sinh viên:\n"
        tsql = 'SELECT * FROM SINHVIEN'
        with self.cursor.execute(tsql) as df:
            for row in df:
                danh_sach += f"Mã SV: {row[0]}\nHọ Tên: {row[1]}\nGiới Tính: {row[2]}\nNgày Sinh: {row[3]}\nLớp: {row[4]}\n\n"
            messagebox.showinfo("Danh Sách Sinh Viên", danh_sach)
    def xem_gv(self):
    def xem_mon(self):

    def verify_masv(self, ma_sv):
        flag = False
        tsql = 'SELECT ID FROM SINHVIEN'
        with self.cursor.execute(tsql) as df:
            for row in df:
                if ma_sv == row[0]:
                    flag = True
                    break
        return flag
    def insert_sv(self):
        ma_sv = self.txt_ma_sv.get()
        ho_ten = self.txt_ho_ten.get()
        gioi_tinh = self.txt_gioi_tinh.get()
        ngay_sinh = self.txt_ngay_sinh.get()
        lop = self.txt_lop.get()

        sv = SinhVien()
        sv.ma_sv_set(ma_sv)
        sv.ho_ten_set(ho_ten)
        sv.gioi_tinh_set(gioi_tinh)
        sv.ngay_sinh_set(ngay_sinh)
        sv.lop_set(lop)

        if self.verify_masv(sv.ma_sv_get()) == True:
            messagebox.showerror("Lỗi", "Mã số sinh viên này da ton tai.")
        else:
            tsql = """INSERT INTO SINHVIEN VALUES ((?),(?),(?),(?),(?))"""
            dob = sv.ngay_sinh_get().split('/')
            dob = datetime.datetime(int(dob[2]), int(dob[1]), int(dob[0]))
            dob.strftime('%d/%m/%y')
            with self.cursor.execute(tsql, sv.masv_get(, sv.ho_ten_get(), sv.ngay_sinh_get(), dob, sv.lop_get()):
                print('Successfully inserted')
                messagebox.showerror("Successfully inserted")






    def insert_gv(self):
    def insert_mon(self):

    def update_...
    def update_...
    def update...

    def delete_sv(self):
    def delete...
    def delete...





if __name__ == '__main__':
