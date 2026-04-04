from .user import create_user
from App.database import db
from .lot import create_lot, edit_lotRFP_details
from .student import create_student
from .admin import create_admin
from App.models import *

def initialize():
    db.drop_all()
    db.create_all()
    
    create_admin("bob", "bobpass")

    create_lot("GIS Lab", "Medium, capable of having 20 machines", 160000.00)
    create_lot("Government Office Lab", "Small, capable of having 10 machines", 110000.00)
    create_lot("University Computer Lab", "Medium, capable of having 30 machines", 250000.00)
    create_lot("Data Center", "Large, capable of having 500 machines", 25000000.00)

    edit_lotRFP_details(1, "Workstation Desktop", "Intel Core i9-13900K", "64GB DDR5", "27-inch 4K IPS", "Windows 11 Pro", "2TB NVMe SSD", "NVIDIA RTX 4080", "4x USB-A, 2x USB-C, HDMI 2.1, DisplayPort 1.4", "Mechanical Keyboard, Ergonomic Mouse, Drawing Tablet", "Webcam, WiFi 6E, Bluetooth 5.2")
    edit_lotRFP_details(2, "Laptop", "AMD Ryzen 7 7745HX", "32GB DDR5", "15.6-inch FHD 144Hz", "Windows 11 Pro / Ubuntu 22.04 Dual Boot", "1TB NVMe SSD", "NVIDIA RTX 3060", "3x USB-A, 2x USB-C, HDMI 2.0, SD Card Reader", "Wireless Keyboard, Wireless Mouse, USB Hub", "Fingerprint Reader, WiFi 6, Bluetooth 5.0")
    edit_lotRFP_details(3, "Desktop PC", "Intel Core i5-13400", "16GB DDR4", "24-inch FHD", "Windows 11 Home", "512GB NVMe SSD", "Intel UHD Graphics 730", "4x USB-A, 1x USB-C, HDMI 1.4, VGA", "Standard Keyboard, Optical Mouse", "Webcam, WiFi 5, Bluetooth 4.2")
    edit_lotRFP_details(4, "High-Performance Workstation", "AMD Ryzen Threadripper 7960X", "128GB DDR5 ECC", "Dual 32-inch 4K", "Ubuntu 22.04 LTS", "4TB NVMe SSD RAID", "NVIDIA RTX 4090 x2", "6x USB-A, 4x USB-C, 2x Thunderbolt 4, Dual Ethernet", "Ergonomic Keyboard, Precision Mouse, USB-C Docking Station", "10GbE Network Card, WiFi 6E, Bluetooth 5.2, Liquid Cooling")

    create_student("jack", "20240123", "jackpass")
    create_student("cooper", "20231245", "cooperpass")
    create_student("john", "20229876", "johnpass")
    create_student("tony", "20235678", "tonypass")

    create_student("peper", "20246789", "peperpass")
    create_student("steve", "20242345", "stevepass")
    create_student("clint", "20238901", "clintpass")
    create_student("bruce", "20238902", "brucepass")