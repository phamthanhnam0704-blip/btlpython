import os

TEN_FILE = "du_lieu_thue_tncn.txt"

def tinh_cac_khoan_giam_tru(so_npt, giam_tru_khac):
    """
    Tính tổng các khoản giảm trừ:
    - Bản thân: 11.000.000 VNĐ/tháng
    - Người phụ thuộc: 4.400.000 VNĐ/người/tháng
    - Giảm trừ khác (bảo hiểm, từ thiện,...)
    """
    gttb = 11_000_000.0
    gt_npt = 4_400_000.0 * so_npt
    return gttb + gt_npt + giam_tru_khac

def tinh_thu_nhap_tinh_thue(thu_nhap, cac_khoan_giam_tru):
    """Tính thu nhập tính thuế = Tổng thu nhập - Tổng giảm trừ (không nhỏ hơn 0)"""
    tntt = thu_nhap - cac_khoan_giam_tru
    return max(0.0, tntt)

def tinh_thue_tncn_luy_tien(thu_nhap_tinh_thue):
    """
    Tính thuế TNCN theo biểu thuế lũy tiến từng phần 7 bậc:
    - Bậc 1 (đến 5tr): 5%
    - Bậc 2 (trên 5tr đến 10tr): 10%
    - Bậc 3 (trên 10tr đến 18tr): 15%
    - Bậc 4 (trên 18tr đến 32tr): 20%
    - Bậc 5 (trên 32tr đến 52tr): 25%
    - Bậc 6 (trên 52tr đến 80tr): 30%
    - Bậc 7 (trên 80tr): 35%
    """
    if thu_nhap_tinh_thue <= 0:
        return 0.0
    
    bac_thue = [
        (5_000_000, 0.05),
        (10_000_000, 0.10),
        (18_000_000, 0.15),
        (32_000_000, 0.20),
        (52_000_000, 0.25),
        (80_000_000, 0.30),
        (float('inf'), 0.35)
    ]
    
    thue_phai_nop = 0.0
    muc_truoc = 0.0
    for muc_tren, thue_suat in bac_thue:
        if thu_nhap_tinh_thue > muc_tren:
            thue_phai_nop += (muc_tren - muc_truoc) * thue_suat
            muc_truoc = muc_tren
        else:
            thue_phai_nop += (thu_nhap_tinh_thue - muc_truoc) * thue_suat
            break
    return round(thue_phai_nop, 2)

def nhap_so_thuc(thong_bao, min_val=0.0):
    """Hàm nhập số thực an toàn, chống crash khi nhập chữ cái"""
    while True:
        try:
            val = float(input(thong_bao))
            if val < min_val:
                print(f"Lỗi: Giá trị không được nhỏ hơn {min_val}. Vui lòng nhập lại!")
            else:
                return val
        except ValueError:
            print("Lỗi: Dữ liệu nhập vào phải là số hợp lệ!")

def nhap_so_nguyen(thong_bao, min_val=0, max_val=20):
    """Hàm nhập số nguyên an toàn cho số người phụ thuộc"""
    while True:
        try:
            val = int(input(thong_bao))
            if val < min_val or val > max_val:
                print(f"Lỗi: Số nguyên phải nằm trong khoảng [{min_val}, {max_val}].")
            else:
                return val
        except ValueError:
            print("Lỗi: Vui lòng nhập số nguyên hợp lệ!")

def tim_kiem_theo_ma(danh_sach, ma_nld):
    """Tìm kiếm nhân sự theo mã (trả về index hoặc -1)"""
    for idx, item in enumerate(danh_sach):
        if item['ma_nld'].upper() == ma_nld.upper():
            return idx
    return -1

# ================= 9 CHỨC NĂNG CỐT LÕI =================

def them_nhan_su(danh_sach):
    print("\n--- THÊM MỚI NHÂN SỰ ---")
    while True:
        ma_nld = input("Nhập mã nhân sự (VD: NV001): ").strip().upper()
        if not ma_nld:
            print("Mã nhân sự không được để trống!")
            continue
        if tim_kiem_theo_ma(danh_sach, ma_nld) != -1:
            print(f"Lỗi: Mã nhân sự '{ma_nld}' đã tồn tại trong hệ thống. Vui lòng nhập mã khác!")
        else:
            break
            
    ho_ten = input("Nhập họ và tên: ").strip().title()
    thu_nhap = nhap_so_thuc("Nhập tổng thu nhập chịu thuế (VNĐ): ")
    so_npt = nhap_so_nguyen("Nhập số người phụ thuộc (0-20): ", 0, 20)
    giam_tru_khac = nhap_so_thuc("Nhập các khoản giảm trừ khác (bảo hiểm, từ thiện...): ")
    
    # Đảm bảo giảm trừ khác không vượt quá tổng thu nhập
    while giam_tru_khac > thu_nhap:
        print("Lỗi: Giảm trừ khác không thể lớn hơn tổng thu nhập!")
        giam_tru_khac = nhap_so_thuc("Nhập lại giảm trừ khác: ")

    giam_tru = tinh_cac_khoan_giam_tru(so_npt, giam_tru_khac)
    tntt = tinh_thu_nhap_tinh_thue(thu_nhap, giam_tru)
    thue = tinh_thue_tncn_luy_tien(tntt)

    record = {
        "ma_nld": ma_nld,
        "ho_ten": ho_ten,
        "thu_nhap": thu_nhap,
        "so_npt": so_npt,
        "giam_tru_khac": giam_tru_khac,
        "cac_khoan_giam_tru": giam_tru,
        "thu_nhap_tinh_thue": tntt,
        "thue_phai_nop": thue
    }
    danh_sach.append(record)
    print(f"Thành công: Đã thêm nhân sự '{ho_ten}' vào hệ thống!")

def hien_thi_danh_sach(danh_sach):
    if not danh_sach:
        print("\nThông báo: Danh sách nhân sự hiện đang trống!")
        return
    
    print("\n" + "="*115)
    print(f"{'DANH SÁCH NHÂN SỰ VÀ TÍNH THUẾ THU NHẬP CÁ NHÂN':^115}")
    print("="*115)
    print(f"{'Mã NV':<8} | {'Họ và tên':<20} | {'Tổng thu nhập':<15} | {'Số NPT':<8} | {'Giảm trừ khác':<15} | {'Thu nhập tính thuế':<18} | {'Thuế phải nộp':<15}")
    print("-" * 115)
    for item in danh_sach:
        print(f"{item['ma_nld']:<8} | {item['ho_ten']:<20} | {item['thu_nhap']:15,.0f} | {item['so_npt']:<8} | {item['giam_tru_khac']:15,.0f} | {item['thu_nhap_tinh_thue']:18,.0f} | {item['thue_phai_nop']:15,.0f}")
    print("="*115)

def cap_nhat_nhan_su(danh_sach):
    print("\n--- CẬP NHẬT THÔNG TIN NHÂN SỰ ---")
    ma_nld = input("Nhập mã nhân sự cần cập nhật: ").strip().upper()
    idx = tim_kiem_theo_ma(danh_sach, ma_nld)
    
    if idx == -1:
        print(f"Không tìm thấy nhân sự có mã '{ma_nld}'!")
        return
        
    item = danh_sach[idx]
    print(f"Đã tìm thấy: {item['ho_ten']}. Nhập thông tin mới (nhấn Enter để giữ nguyên giá trị cũ):")
    
    ten_moi = input(f"Họ tên mới [{item['ho_ten']}]: ").strip()
    if ten_moi:
        item['ho_ten'] = ten_moi.title()
        
    thu_nhap_str = input(f"Tổng thu nhập mới [{item['thu_nhap']}]: ").strip()
    if thu_nhap_str:
        item['thu_nhap'] = float(thu_nhap_str)
        
    npt_str = input(f"Số NPT mới [{item['so_npt']}]: ").strip()
    if npt_str:
        item['so_npt'] = int(npt_str)
        
    gtk_str = input(f"Giảm trừ khác mới [{item['giam_tru_khac']}]: ").strip()
    if gtk_str:
        item['giam_tru_khac'] = float(gtk_str)
        
    # Tính toán lại tự động
    item['cac_khoan_giam_tru'] = tinh_cac_khoan_giam_tru(item['so_npt'], item['giam_tru_khac'])
    item['thu_nhap_tinh_thue'] = tinh_thu_nhap_tinh_thue(item['thu_nhap'], item['cac_khoan_giam_tru'])
    item['thue_phai_nop'] = tinh_thue_tncn_luy_tien(item['thu_nhap_tinh_thue'])
    
    print("Thành công: Đã cập nhật thông tin và tính toán lại thuế cho nhân sự!")

def xoa_nhan_su(danh_sach):
    print("\n--- XÓA NHÂN SỰ ---")
    ma_nld = input("Nhập mã nhân sự cần xóa: ").strip().upper()
    idx = tim_kiem_theo_ma(danh_sach, ma_nld)
    
    if idx == -1:
        print(f"Không tìm thấy nhân sự có mã '{ma_nld}'!")
        return
        
    item = danh_sach[idx]
    print(f"Xác nhận xóa nhân sự: {item['ma_nld']} - {item['ho_ten']}?")
    xac_nhan = input("Nhập 'Y' để đồng ý xóa, phím khác để hủy: ").strip().upper()
    if xac_nhan == 'Y':
        danh_sach.pop(idx)
        print("Thành công: Đã xóa nhân sự khỏi hệ thống!")
    else:
        print("Đã hủy thao tác xóa.")

def tim_kiem_nhan_su(danh_sach):
    if not danh_sach:
        print("\nDanh sách trống!")
        return
    print("\n--- TÌM KIẾM NHÂN SỰ ---")
    print("1. Tìm chính xác theo mã nhân sự")
    print("2. Tìm gần đúng theo họ tên")
    print("3. Tìm theo khoảng thu nhập")
    chon = input("Chọn phương thức (1-3): ").strip()
    
    if chon == '1':
        ma = input("Nhập mã nhân sự: ").strip().upper()
        idx = tim_kiem_theo_ma(danh_sach, ma)
        if idx != -1:
            hien_thi_danh_sach([danh_sach[idx]])
        else:
            print("Không tìm thấy!")
    elif chon == '2':
        tu_khoa = input("Nhập từ khóa tên cần tìm: ").strip().lower()
        ket_qua = [x for x in danh_sach if tu_khoa in x['ho_ten'].lower()]
        if ket_qua:
            hien_thi_danh_sach(ket_qua)
        else:
            print("Không tìm thấy nhân sự phù hợp!")
    elif chon == '3':
        min_tn = nhap_so_thuc("Nhập thu nhập tối thiểu: ")
        max_tn = nhap_so_thuc("Nhập thu nhập tối đa: ")
        ket_qua = [x for x in danh_sach if min_tn <= x['thu_nhap'] <= max_tn]
        if ket_qua:
            hien_thi_danh_sach(ket_qua)
        else:
            print("Không có nhân sự nào trong khoảng thu nhập này!")

def sap_xep_danh_sach(danh_sach):
    if not danh_sach:
        print("\nDanh sách trống!")
        return
    print("\n--- SẮP XẾP DANH SÁCH ---")
    print("1. Sắp xếp theo Tổng thu nhập")
    print("2. Sắp xếp theo Thuế phải nộp")
    tieu_chi = input("Chọn tiêu chí (1-2): ").strip()
    
    print("Chiều sắp xếp:")
    print("1. Tăng dần (Ascending)")
    print("2. Giảm dần (Descending)")
    chieu = input("Chọn chiều (1-2): ").strip()
    
    reverse = True if chieu == '2' else False
    key_field = 'thu_nhap' if tieu_chi == '1' else 'thue_phai_nop'
    
    danh_sach.sort(key=lambda x: x[key_field], reverse=reverse)
    print("Thành công: Đã sắp xếp lại danh sách!")
    hien_thi_danh_sach(danh_sach)

def thong_ke_tai_chinh(danh_sach):
    if not danh_sach:
        print("\nDanh sách trống, không thể thống kê!")
        return
        
    tong_ns = len(danh_sach)
    tong_thu_nhap = sum(x['thu_nhap'] for x in danh_sach)
    tong_giam_tru = sum(x['cac_khoan_giam_tru'] for x in danh_sach)
    tong_tntt = sum(x['thu_nhap_tinh_thue'] for x in danh_sach)
    tong_thue = sum(x['thue_phai_nop'] for x in danh_sach)
    tb_thu_nhap = tong_thu_nhap / tong_ns
    
    max_thu_nhap = max(danh_sach, key=lambda x: x['thu_nhap'])
    max_thue = max(danh_sach, key=lambda x: x['thue_phai_nop'])
    
    co_nop_thue = sum(1 for x in danh_sach if x['thue_phai_nop'] > 0)
    khong_nop_thue = tong_ns - co_nop_thue

    print("\n" + "="*55)
    print(f"{'BÁO CÁO THỐNG KÊ TÀI CHÍNH NHÂN SỰ':^55}")
    print("="*55)
    print(f"1. Tổng số nhân sự trong đơn vị         : {tong_ns} người")
    print(f"2. Tổng thu nhập chịu thuế              : {tong_thu_nhap:,.0f} VNĐ")
    print(f"3. Tổng các khoản giảm trừ              : {tong_giam_tru:,.0f} VNĐ")
    print(f"4. Tổng thu nhập tính thuế              : {tong_tntt:,.0f} VNĐ")
    print(f"5. Tổng số tiền thuế TNCN phải nộp      : {tong_thue:,.0f} VNĐ")
    print(f"6. Thu nhập bình quân / nhân sự         : {tb_thu_nhap:,.0f} VNĐ")
    print(f"7. Nhân sự có thu nhập cao nhất         : {max_thu_nhap['ho_ten']} ({max_thu_nhap['thu_nhap']:,.0f} VNĐ)")
    print(f"8. Nhân sự nộp thuế cao nhất            : {max_thue['ho_ten']} ({max_thue['thue_phai_nop']:,.0f} VNĐ)")
    print(f"9. Tỷ lệ nhân sự phải nộp thuế          : {(co_nop_thue/tong_ns)*100:.1f}% ({co_nop_thue}/{tong_ns} người)")
    print(f"10. Tỷ lệ nhân sự không phải nộp thuế   : {(khong_nop_thue/tong_ns)*100:.1f}% ({khong_nop_thue}/{tong_ns} người)")
    print("="*55)

def luu_du_lieu(danh_sach):
    try:
        with open(TEN_FILE, "w", encoding="utf-8") as f:
            for item in danh_sach:
                line = f"{item['ma_nld']}|{item['ho_ten']}|{item['thu_nhap']}|{item['so_npt']}|{item['giam_tru_khac']}\n"
                f.write(line)
        print(f"Thành công: Đã lưu {len(danh_sach)} bản ghi vào tệp '{TEN_FILE}'.")
    except Exception as e:
        print(f"Lỗi khi ghi tệp: {e}")

def doc_du_lieu(danh_sach):
    if not os.path.exists(TEN_FILE):
        print(f"Thông báo: Tệp '{TEN_FILE}' chưa tồn tại.")
        return
    try:
        with open(TEN_FILE, "r", encoding="utf-8") as f:
            danh_sach.clear()
            for line in f:
                parts = line.strip().split("|")
                if len(parts) == 5:
                    ma = parts[0].strip().upper()
                    ten = parts[1].strip()
                    thu_nhap = float(parts[2])
                    so_npt = int(parts[3])
                    gtk = float(parts[4])
                    
                    giam_tru = tinh_cac_khoan_giam_tru(so_npt, gtk)
                    tntt = tinh_thu_nhap_tinh_thue(thu_nhap, giam_tru)
                    thue = tinh_thue_tncn_luy_tien(tntt)
                    
                    record = {
                        "ma_nld": ma,
                        "ho_ten": ten,
                        "thu_nhap": thu_nhap,
                        "so_npt": so_npt,
                        "giam_tru_khac": gtk,
                        "cac_khoan_giam_tru": giam_tru,
                        "thu_nhap_tinh_thue": tntt,
                        "thue_phai_nop": thue
                    }
                    danh_sach.append(record)
        print(f"Thành công: Đã đọc {len(danh_sach)} bản ghi từ tệp '{TEN_FILE}'.")
    except Exception as e:
        print(f"Lỗi khi đọc tệp: {e}")

# ================= HỆ THỐNG MENU CHÍNH =================

def main():
    danh_sach_nhan_su = []
    # Tự động nạp dữ liệu cũ nếu có khi khởi động chương trình
    doc_du_lieu(danh_sach_nhan_su)
    
    while True:
        print("\n" + "="*50)
        print(f"{'QUẢN LÝ THUẾ THU NHẬP CÁ NHÂN (PYTHON)':^50}")
        print("="*50)
        print("1. Thêm mới nhân sự")
        print("2. Hiển thị danh sách nhân sự")
        print("3. Cập nhật thông tin nhân sự")
        print("4. Xóa nhân sự")
        print("5. Tìm kiếm nhân sự")
        print("6. Sắp xếp danh sách")
        print("7. Thống kê & Báo cáo tài chính")
        print("8. Lưu dữ liệu xuống tệp (.txt)")
        print("9. Đọc dữ liệu từ tệp (.txt)")
        print("0. Thoát chương trình")
        print("="*50)
        
        chon = input("Nhập lựa chọn của bạn (0-9): ").strip()
        
        if chon == '1':
            them_nhan_su(danh_sach_nhan_su)
        elif chon == '2':
            hien_thi_danh_sach(danh_sach_nhan_su)
        elif chon == '3':
            cap_nhat_nhan_su(danh_sach_nhan_su)
        elif chon == '4':
            xoa_nhan_su(danh_sach_nhan_su)
        elif chon == '5':
            tim_kiem_nhan_su(danh_sach_nhan_su)
        elif chon == '6':
            sap_xep_danh_sach(danh_sach_nhan_su)
        elif chon == '7':
            thong_ke_tai_chinh(danh_sach_nhan_su)
        elif chon == '8':
            luu_du_lieu(danh_sach_nhan_su)
        elif chon == '9':
            doc_du_lieu(danh_sach_nhan_su)
        elif chon == '0':
            # Tự động lưu file trước khi thoát
            luu_du_lieu(danh_sach_nhan_su)
            print("\nCảm ơn bạn đã sử dụng chương trình. Tạm biệt!")
            break
        else:
            print("Lỗi: Lựa chọn không hợp lệ! Vui lòng chọn từ 0 đến 9.")

if __name__ == "__main__":
    main()