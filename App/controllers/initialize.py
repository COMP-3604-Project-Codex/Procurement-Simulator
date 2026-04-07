from App.controllers.studentGroup import add_studentGroup

from .user import create_user
from App.database import db
from .lot import create_lot, edit_lotRFP_details
from .student import create_student
from .admin import create_admin
from .group import create_group
from App.models import *

def initialize():
    db.drop_all()
    db.create_all()
    
    create_admin("bob", "bobpass")

    create_lot("GIS Lab", "Medium, capable of having 20 machines", 160000.00)
    create_lot("Government Office Lab", "Small, capable of having 10 machines", 110000.00)
    create_lot("University Computer Lab", "Medium, capable of having 30 machines", 250000.00)
    create_lot("Data Center", "Large, capable of having 500 machines", 25000000.00)
    create_lot("Medical Imaging Lab", "Medium, capable of having 15 machines", 320000.00)
    create_lot("Architecture & Design Studio", "Small, capable of having 12 machines", 195000.00)

    edit_lotRFP_details(1, deviceType="Workstation Desktop", cpu="Intel Core i9-13900K", ram="64GB DDR5", resolution="27-inch 4K IPS", os="Windows 11 Pro", drive="2TB NVMe SSD", gpu="NVIDIA RTX 4080", peripherals="4x USB-A, 2x USB-C, HDMI 2.1, DisplayPort 1.4", features="Mechanical Keyboard, Ergonomic Mouse, Drawing Tablet", io="Webcam, WiFi 6E, Bluetooth 5.2")
    edit_lotRFP_details(2, deviceType="Laptop", cpu="AMD Ryzen 7 7745HX", ram="32GB DDR5", resolution="15.6-inch FHD 144Hz", os="Windows 11 Pro / Ubuntu 22.04 Dual Boot", drive="1TB NVMe SSD", gpu="NVIDIA RTX 3060", peripherals="3x USB-A, 2x USB-C, HDMI 2.0, SD Card Reader", features="Wireless Keyboard, Wireless Mouse, USB Hub", io="Fingerprint Reader, WiFi 6, Bluetooth 5.0")
    edit_lotRFP_details(3, deviceType="Desktop PC", cpu="Intel Core i5-13400", ram="16GB DDR4", resolution="24-inch FHD", os="Windows 11 Home", drive="512GB NVMe SSD", gpu="Intel UHD Graphics 730", peripherals="4x USB-A, 1x USB-C, HDMI 1.4, VGA", features="Standard Keyboard, Optical Mouse", io="Webcam, WiFi 5, Bluetooth 4.2")
    edit_lotRFP_details(4, deviceType="High-Performance Workstation", cpu="AMD Ryzen Threadripper 7960X", ram="128GB DDR5 ECC", resolution="Dual 32-inch 4K", os="Ubuntu 22.04 LTS", drive="4TB NVMe SSD RAID", gpu="NVIDIA RTX 4090 x2", peripherals="6x USB-A, 4x USB-C, 2x Thunderbolt 4, Dual Ethernet", features="Ergonomic Keyboard, Precision Mouse, USB-C Docking Station", io="10GbE Network Card, WiFi 6E, Bluetooth 5.2, Liquid Cooling")
    edit_lotRFP_details(5, deviceType="High-Performance Workstation", cpu="Intel Xeon W-2295", ram="128GB DDR4 ECC", resolution="Dual 27-inch 4K IPS", os="Windows 11 Pro", drive="2TB NVMe SSD + 4TB HDD", gpu="NVIDIA RTX A5000", peripherals="6x USB-A, 4x USB-C, 2x Thunderbolt 3, Dual Ethernet", features="Medical-Grade Mouse, Ergonomic Keyboard, 3D Connexion SpaceMouse", io="DICOM Compatibility, WiFi 6E, Bluetooth 5.2, ECC Memory Support")
    edit_lotRFP_details(6, deviceType="High-End Desktop", cpu="Intel Core i9-13900K", ram="64GB DDR5", resolution="Dual 32-inch 4K OLED", os="Windows 11 Pro", drive="2TB NVMe SSD + 2TB HDD", gpu="NVIDIA RTX 4090", peripherals="4x USB-A, 4x USB-C, 2x Thunderbolt_4, SD Card Reader", features="Wireless Ergonomic Keyboard, Precision Mouse, Drawing Tablet (Wacom)", io="Pantone-Calibrated Display, WiFi_6E, Bluetooth_5.2, Hardware Color Calibrator")


    create_student("Aiden Joseph", "20240001", "aidenpass")
    create_student("Kareem Ali", "20240002", "kareempass")
    create_student("Joshua Peters", "20240003", "joshuapass")
    create_student("Daniel Roberts", "20240004", "danielpass")

    create_student("Samantha Clarke", "20240005", "samanthapass")
    create_student("Aaliyah Mohammed", "20240006", "aaliyahpass")
    create_student("Leah Charles", "20240007", "leahpass")
    create_student("Naomi Thomas", "20240008", "naomipass")

    create_student("Ryan Williams", "20240009", "ryanpass")
    create_student("Darius Edwards", "20240010", "dariuspass")
    create_student("Marcus Browne", "20240011", "marcuspass")
    create_student("Andre Lewis", "20240012", "andrepass")

    create_student("Keisha Grant", "20240013", "keishapass")
    create_student("Tricia Ramnarine", "20240014", "triciapass")
    create_student("Anil Singh", "20240015", "anilpass")
    create_student("Ravi Persad", "20240016", "ravipass")

    create_student("Janelle Baptiste", "20240017", "janellepass")
    create_student("Shawn Mitchell", "20240018", "shawnpass")
    create_student("Kevin Hernandez", "20240019", "kevinpass")
    create_student("Ashley Gomez", "20240020", "ashleypass")

    # Group 1
    group1 = create_group("NexoraTech")
    s1 = db.session.scalars(db.select(Student).where(Student.username == "20240001")).first()
    s2 = db.session.scalars(db.select(Student).where(Student.username == "20240002")).first()
    s3 = db.session.scalars(db.select(Student).where(Student.username == "20240003")).first()

    members1 = [s1.id, s2.id, s3.id]
    for member in members1:
        add_studentGroup(member, group1.id)


    # Group 2
    group2 = create_group("QuantumSoft")
    s4 = db.session.scalars(db.select(Student).where(Student.username == "20240004")).first()
    s5 = db.session.scalars(db.select(Student).where(Student.username == "20240005")).first()
    s6 = db.session.scalars(db.select(Student).where(Student.username == "20240006")).first()

    members2 = [s4.id, s5.id, s6.id]
    for member in members2:
        add_studentGroup(member, group2.id)


    # Group 3
    group3 = create_group("ByteForge")
    s7 = db.session.scalars(db.select(Student).where(Student.username == "20240007")).first()
    s8 = db.session.scalars(db.select(Student).where(Student.username == "20240008")).first()
    s9 = db.session.scalars(db.select(Student).where(Student.username == "20240009")).first()

    members3 = [s7.id, s8.id, s9.id]
    for member in members3:
        add_studentGroup(member, group3.id)


    # Group 4
    group4 = create_group("CyberNova")
    s10 = db.session.scalars(db.select(Student).where(Student.username == "20240010")).first()
    s11 = db.session.scalars(db.select(Student).where(Student.username == "20240011")).first()
    s12 = db.session.scalars(db.select(Student).where(Student.username == "20240012")).first()

    members4 = [s10.id, s11.id, s12.id]
    for member in members4:
        add_studentGroup(member, group4.id)