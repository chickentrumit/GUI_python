import tkinter as tk
import datetime
import pyodbc
from tkinter import messagebox


class SinhVien:
    def __init__(self, ma_sv, ho_ten, gioi_tinh, ngay_sinh, lop):
        self.ma_sv = ma_sv
        self.ho_ten = ho_ten
        self.gioi_tinh = gioi_tinh
        self.ngay_sinh = ngay_sinh
        self.lop = lop


class QuanLySinhVienGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Quản Lý Sinh Viên")
        self.window.geometry("1250x700+150+50")
        self.create_gui()

        self.sinh_vien_list = []

    def create_gui(self):
        # Tạo các đối tượng GUI
        self.lbl_ma_sv = tk.Label(self.window, text="Mã SV:")
        self.lbl_ma_sv.grid(row=17, column=30, padx=5, pady=5)
        self.txt_ma_sv = tk.Entry(self.window)
        self.txt_ma_sv.grid(row=17, column=31, padx=5, pady=5)

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

    def them_sinh_vien(self):
        # Lấy thông tin sinh viên từ các ô nhập liệu
        ma_sv = self.txt_ma_sv.get()
        ho_ten = self.txt_ho_ten.get()
        gioi_tinh = self.txt_gioi_tinh.get()
        ngay_sinh = self.txt_ngay_sinh.get()
        lop = self.txt_lop.get()

        # Kiểm tra thông tin đã nhập đủ chưa
        if ma_sv == "" or ho_ten == "" or gioi_tinh == "" or ngay_sinh == "" or lop == "":
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin sinh viên.")
        else:
            # Tạo đối tượng sinh viên mới
            sinh_vien = SinhVien(ma_sv, ho_ten, gioi_tinh, ngay_sinh, lop)
            # Thêm sinh viên vào danh sách
            self.sinh_vien_list.append(sinh_vien)
            # Cập nhật giao diện
            self.lbl_ket_qua.config(text="Thêm sinh viên thành công.")
            self.insertdb()
            # Xóa dữ liệu trên các ô nhập liệu
            self.clear_input()

    def xem_sinh_vien(self):
        # Hiển thị danh sách sinh viên trong MessageBox
        danh_sach = "Danh sách sinh viên:\n"
        tsql = 'SELECT * FROM SINHVIEN'
        with cursor.execute(tsql) as df:
            for i in df:
                danh_sach += f"Mã SV: {i[0]}\nHọ Tên: {i[1]}\nGiới Tính: {i[2]}\nNgày Sinh: {i[3]}\nLớp: {i[4]}\n\n"
            messagebox.showinfo("Danh Sách Sinh Viên", danh_sach)

    def cap_nhat_sinh_vien(self):
        # Lấy mã sinh viên từ ô nhập liệu
        ma_sv = self.txt_ma_sv.get()

        flag = None
        tsql = 'SELECT ID FROM SINHVIEN'
        with cursor.execute(tsql) as f:
            for sv in f:
                if int(ma_sv) == sv[0]:
                    ho_ten = self.txt_ho_ten.get()
                    gioi_tinh = self.txt_gioi_tinh.get()
                    ngay_sinh = self.txt_ngay_sinh.get()
                    lop = self.txt_lop.get()
                    self.update_delete(ma_sv, ho_ten, gioi_tinh, ngay_sinh, lop, 'update')
                    self.lbl_ket_qua.config(text="update sinh viên thành công.")
                    # Xóa dữ liệu trên các ô nhập liệu
                    self.clear_input()
                    flag = True
                    # Cập nhật giao diện
                    self.lbl_ket_qua.config(text="Cập nhật thông tin sinh viên thành công.")
                    break

        # Nếu sinh viên không tồn tại, hiển thị thông báo lỗi
        if flag is None:
            messagebox.showerror("Lỗi", "Không tìm thấy sinh viên có mã số sinh viên này.")
            # Xóa dữ liệu trên các ô nhập liệu
            self.clear_input()

    def xoa_sinh_vien(self):
        # Lấy mã sinh viên từ ô nhập liệu
        ma_sv = self.txt_ma_sv.get()

        # Tìm sinh viên trong danh sách
        flag = None
        tsql = 'SELECT ID FROM SINHVIEN'
        with cursor.execute(tsql) as f:
            for sv in f:
                if int(ma_sv) == sv[0]:
                    self.update_delete(ma_sv, 'delete')
                    self.lbl_ket_qua.config(text="Xóa sinh viên thành công.")
                    # Xóa dữ liệu trên các ô nhập liệu
                    self.clear_input()
                    flag = True
                    break

        # Nếu sinh viên không tồn tại, hiển thị thông báo lỗi
        if flag is None:
            messagebox.showerror("Lỗi", "Không tìm thấy sinh viên có mã số sinh viên này.")

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

    def insertdb(self):
        for i in self.sinh_vien_list:
            tsql = """INSERT INTO SINHVIEN VALUES ((?),(?),(?),(?),(?))"""
            dob = i.ngay_sinh.split('/')
            dob = datetime.datetime(int(dob[2]), int(dob[1]), int(dob[0]))
            dob.strftime('%d/%m/%y')
            with cursor.execute(tsql, i.ma_sv, i.ho_ten, i.gioi_tinh, dob, i.lop):
                print('Successfully inserted')

    def update_delete(self, ma_sv, operation, ho_ten=None, gioi_tinh=None, ngay_sinh=None, lop=None):
        if operation == 'update':
            tsql = """update SINHVIEN
                    set hoten=?,GIoiTinh=?,ngaysinh=?,class=?
                    where ID=?"""
            with cursor.execute(tsql, ho_ten, gioi_tinh, ngay_sinh, lop, ma_sv):
                print('Successfully updated')
        else:
            tsql = """delete from SINHVIEN where ID=?"""
            with cursor.execute(tsql, ma_sv):
                print('Successfully deleted')


if __name__ == '__main__':
    sv = 'DESKTOP-GTIDRT8'
    dbs = 'QLSV'
    usr = 'sa'
    pwd = 'sa'
    dbs = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + sv + ';DATABASE=' + dbs + ';UID=' + usr + ';PWD=' + pwd + ';autocommit=True')
    cursor = dbs.cursor()

    gui = QuanLySinhVienGUI()
    gui.run()

    cursor.close()

