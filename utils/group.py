def group_post(ngay):
    bin_1={"NhanRac":"box_cardboard_paper","KhoiLuong":0}
    kl_1,kl_2,kl_3,kl_4=0,0,0,0
    bin_2={"NhanRac":"glass_metal_plastic","KhoiLuong":0}
    bin_3={"NhanRac":"organic","KhoiLuong":0}
    bin_4={"NhanRac":"other","KhoiLuong":0}
    newngay=[]
    for d in ngay:
        if d["TenNhan"]=="box_cardboard_paper":
            bin_1['ID_khoangrac']=d['ID_khoangrac']
            bin_1["KhoiLuong"]+=d["KhoiLuong"]
        elif d["TenNhan"]=="glass_metal_plastic":
            bin_2["KhoiLuong"]+=d["KhoiLuong"]
        elif d["TenNhan"]=="organic":
            bin_3["KhoiLuong"]+=d["KhoiLuong"]
        else: 
            bin_4["KhoiLuong"]+=d["KhoiLuong"]
    newngay.append(bin_1)
    newngay.append(bin_2)
    newngay.append(bin_3)
    newngay.append(bin_4)
    return newngay
def group_get(lskhuvuc):
    bin_1={"NhanRac":"box_cardboard_paper","KhoiLuong":0}
    bin_2={"NhanRac":"glass_metal_plastic","KhoiLuong":0}
    bin_3={"NhanRac":"organic","KhoiLuong":0}
    bin_4={"NhanRac":"other","KhoiLuong":0}
    newngay=[]
    for d in lskhuvuc:
        if d["TenNhan"]=="box_cardboard_paper":
            bin_1['ID_khoangrac']=d['ID_khoangrac']
            bin_1["KhoiLuong"]+=d["KhoiLuong"]
        elif d["TenNhan"]=="glass_metal_plastic":
            bin_2['ID_khoangrac']=d['ID_khoangrac']
            bin_2["KhoiLuong"]+=d["KhoiLuong"]
        elif d["TenNhan"]=="organic":
            bin_3['ID_khoangrac']=d['ID_khoangrac']
            bin_3["KhoiLuong"]+=d["KhoiLuong"]
        else: 
            bin_1['ID_khoangrac']=d['ID_khoangrac']
            bin_4["KhoiLuong"]+=d["KhoiLuong"]
    newngay.append(bin_1)
    newngay.append(bin_2)
    newngay.append(bin_3)
    newngay.append(bin_4)
    return newngay