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


    create_student("jack", "20240123", "jackpass")
    create_student("cooper", "20231245", "cooperpass")
    create_student("john", "20229876", "johnpass")
    create_student("ray", "20246789", "raypass")

    create_student("tony", "20235678", "tonypass")
    create_student("steve", "20242345", "stevepass")
    create_student("clint", "20238901", "clintpass")
    create_student("bruce", "20238902", "brucepass")

    create_student("ultron", "20264789", "ultronpass")
    create_student("thanos", "20242435", "thanospass")
    create_student("loki", "20328901", "lokipass")
    create_student("red skull", "20235342", "redskullpass")

    group = create_group("Avengers")
    tony = db.session.scalars(db.select(Student).where(Student.username == "20235678")).first()
    steve = db.session.scalars(db.select(Student).where(Student.username == "20242345")).first()
    clint = db.session.scalars(db.select(Student).where(Student.username == "20238901")).first()
    bruce = db.session.scalars(db.select(Student).where(Student.username == "20238902")).first()   
    members = [tony.id, steve.id, clint.id, bruce.id]

    for member in members:
        add_studentGroup(member, group.id)

    ultron = db.session.scalars(db.select(Student).where(Student.username == "20264789")).first()
    thanos = db.session.scalars(db.select(Student).where(Student.username == "20242435")).first()
    loki = db.session.scalars(db.select(Student).where(Student.username == "20328901")).first()
    red_skull = db.session.scalars(db.select(Student).where(Student.username == "20235342")).first()
    group1 = create_group("Villains")
    members1 = [ultron.id, thanos.id, loki.id, red_skull.id]

    for member in members1:
        add_studentGroup(member, group1.id)

    