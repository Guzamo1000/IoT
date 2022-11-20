def group_post(ngay):
    bin_1={"NhanRac":"box_cardboard_paper","KhoiLuong":0,"AnhRac": None}
    kl_1,kl_2,kl_3,kl_4=0,0,0,0
    bin_2={"NhanRac":"glass_metal_plastic","KhoiLuong":0,"AnhRac": None}
    bin_3={"NhanRac":"organic","KhoiLuong":0,"AnhRac": None}
    bin_4={"NhanRac":"other","KhoiLuong":0,"AnhRac": None}
    newngay=[]
    for d in ngay:
        if d["TenNhan"]=="box_cardboard_paper":
            bin_1['AnhRac']=d['AnhRac']
            bin_1["KhoiLuong"]+=d["KhoiLuong"]
        elif d["TenNhan"]=="glass_metal_plastic":
            bin_2['AnhRac']=d['AnhRac']
            bin_2["KhoiLuong"]+=d["KhoiLuong"]
        elif d["TenNhan"]=="organic":
            bin_3['AnhRac']=d['AnhRac']
            bin_3["KhoiLuong"]+=d["KhoiLuong"]
        else: 
            bin_4['AnhRac']=d['AnhRac']
            bin_4["KhoiLuong"]+=d["KhoiLuong"]
    newngay.append(bin_1)
    newngay.append(bin_2)
    newngay.append(bin_3)
    newngay.append(bin_4)
    return newngay
def group_get(lskhuvuc):
    bin_1={"NhanRac":"box_cardboard_paper","KhoiLuong":0,"ID_khoangrac":None, "AnhRac": None}
    kl_1,kl_2,kl_3,kl_4=0,0,0,0
    bin_2={"NhanRac":"glass_metal_plastic","KhoiLuong":0, "ID_khoangrac":None, "AnhRac":None}
    bin_3={"NhanRac":"organic","KhoiLuong":0, "ID_khoangrac":None, "AnhRac":None}
    bin_4={"NhanRac":"other","KhoiLuong":0 ,"ID_khoangrac":None , "AnhRac":None}
    newngay=[]
    for d in lskhuvuc:
        if d["TenNhan"]=="box_cardboard_paper":
            # bin_1['AnhRac']=d['AnhRac']
            bin_1['ID_khoangrac']=d['ID_khoangrac']
            bin_1["KhoiLuong"]+=d["KhoiLuong"]
        elif d["TenNhan"]=="glass_metal_plastic":
            # bin_2['AnhRac']=d['AnhRac']
            bin_2['ID_khoangrac']=d['ID_khoangrac']
            bin_2["KhoiLuong"]+=d["KhoiLuong"]
        elif d["TenNhan"]=="organic":
            # bin_3['AnhRac']=d['AnhRac']
            bin_3["KhoiLuong"]+=d["KhoiLuong"]
            bin_3['ID_khoangrac']=d['ID_khoangrac']
        else: 
            # bin_4['AnhRac']=d['AnhRac']
            bin_4['ID_khoangrac']=d['ID_khoangrac']
            bin_4["KhoiLuong"]+=d["KhoiLuong"]
    newngay.append(bin_1)
    newngay.append(bin_2)
    newngay.append(bin_3)
    newngay.append(bin_4)
    return newngay