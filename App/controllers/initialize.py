from App.controllers.studentGroup import add_studentGroup

from .user import create_user
from App.database import db
from .lot import create_lot, edit_lotRFP_details
from .labType import create_lab_type
from .student import create_student
from .admin import create_admin
from .group import create_group, approve_group
from .lotGroup import add_lotGroup
from .rfp import create_rfp, approve_rfp
from .bid import create_bid
from .evaluation import create_evaluation, select_evaluation
from App.models import *
import io

def initialize():
    db.drop_all()
    db.create_all()
    
    create_admin("bob", "bobpass")

    gis_type = create_lab_type("GIS Lab", "Medium, capable of having 20 machines")
    government_type = create_lab_type("Government Office Lab", "Small, capable of having 10 machines")
    university_type = create_lab_type("University Computer Lab", "Medium, capable of having 30 machines")
    data_center_type = create_lab_type("Data Center", "Large, capable of having 500 machines")
    medical_type = create_lab_type("Medical Imaging Lab", "Medium, capable of having 15 machines")
    design_type = create_lab_type("Architecture & Design Studio", "Small, capable of having 12 machines")

    create_lot(gis_type.name, gis_type.description, 160000.00, labTypeId=gis_type.id)
    create_lot(government_type.name, government_type.description, 110000.00, labTypeId=government_type.id)
    create_lot(university_type.name, university_type.description, 250000.00, labTypeId=university_type.id)
    create_lot(data_center_type.name, data_center_type.description, 25000000.00, labTypeId=data_center_type.id)
    create_lot(medical_type.name, medical_type.description, 320000.00, labTypeId=medical_type.id)
    create_lot(design_type.name, design_type.description, 195000.00, labTypeId=design_type.id)

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
    create_student("Joey Patterson", "20240021", "joeypass")
    create_student("Michelle James", "20240022", "michellepass")
    create_student("Tyrell George", "20240023", "tyrellpass")
    create_student("Nadia Richards", "20240024", "nadiapass")
    create_student("Jerome Phillips", "20240025", "jeromepass")
    create_student("Vanessa Edwards", "20240026", "vanessapass")
    create_student("Christopher Lewis", "20240027", "christopherpass")
    create_student("Melissa Clarke", "20240028", "melissapass")
    create_student("Devon Peters", "20240029", "devonpass")
    create_student("Sherisse Joseph", "20240030", "sherissepass")
    create_student("Darren Mitchell", "20240031", "darrenpass")

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

    # Group 5
    group5 = create_group("InnovateTech")
    s13 = db.session.scalars(db.select(Student).where(Student.username == "20240013")).first()
    s14 = db.session.scalars(db.select(Student).where(Student.username == "20240014")).first()
    s15 = db.session.scalars(db.select(Student).where(Student.username == "20240015")).first()

    members5 = [s13.id, s14.id, s15.id]
    for member in members5:
        add_studentGroup(member, group5.id)

    # Group 6
    group6 = create_group("CloudSystems")
    s16 = db.session.scalars(db.select(Student).where(Student.username == "20240016")).first()
    s17 = db.session.scalars(db.select(Student).where(Student.username == "20240017")).first()
    s18 = db.session.scalars(db.select(Student).where(Student.username == "20240018")).first()

    members6 = [s16.id, s17.id, s18.id]
    for member in members6:
        add_studentGroup(member, group6.id)

    # Approve groups and assign lots
    approve_group(group1.id)
    add_lotGroup(1, group1.id)
    add_lotGroup(2, group1.id)

    approve_group(group2.id)
    add_lotGroup(3, group2.id)
    add_lotGroup(4, group2.id)

    approve_group(group3.id)
    add_lotGroup(5, group3.id)
    add_lotGroup(6, group3.id)

    # Create sample RFPs
    rfp1_1 = create_rfp(group1.id, 1)
    rfp1_2 = create_rfp(group1.id, 2)
    rfp2_3 = create_rfp(group2.id, 3)
    rfp2_4 = create_rfp(group2.id, 4)

    # Approve some RFPs
    approve_rfp(group1.id, 1)
    approve_rfp(group1.id, 2)
    approve_rfp(group2.id, 3)

    group6

    # Generate sample PDF content
    def generate_sample_pdf(vendor_name, lot_name, price):
        pdf_header = b'%PDF-1.4\n'
        pdf_content = (
            f'Sample Bid Document\nVendor: {vendor_name}\nLot: {lot_name}\n'
            f'Quoted Price: ${price:,.2f}\n\n'
            f'This is a sample bid document for testing purposes.\n'
            f'Terms and conditions apply.\n'
        ).encode('latin1')
        pdf_footer = b'%%EOF\n'
        return pdf_header + pdf_content + pdf_footer

    # Create sample bids
    bid1 = create_bid(1, group2.id, group1.id, generate_sample_pdf("QuantumSoft", "GIS Lab", 145000), "quantumsoft_gis_bid.pdf", 145000.00)
    bid2 = create_bid(1, group3.id, group1.id, generate_sample_pdf("ByteForge", "GIS Lab", 155000), "byteforge_gis_bid.pdf", 155000.00)
    bid3 = create_bid(2, group2.id, group1.id, generate_sample_pdf("QuantumSoft", "Gov Office Lab", 105000), "quantumsoft_gov_bid.pdf", 105000.00)
    bid4 = create_bid(3, group1.id, group2.id, generate_sample_pdf("NexoraTech", "University Lab", 240000), "nexoratech_uni_bid.pdf", 240000.00)
    bid5 = create_bid(3, group3.id, group2.id, generate_sample_pdf("CyberNova", "University Lab", 260000), "cybernova_uni_bid.pdf", 260000.00)
    bid6 = create_bid(4, group1.id, group2.id, generate_sample_pdf("NexoraTech", "Data Center", 24950000), "nexoratech_dc_bid.pdf", 24950000.00)

    # Create sample evaluations for draft status
    eval1 = create_evaluation(group1.id, group2.id, bid1.id, 1, 4, 3, 4, 3)
    eval2 = create_evaluation(group1.id, group3.id, bid2.id, 1, 5, 4, 5, 4)
    eval3 = create_evaluation(group1.id, group2.id, bid3.id, 2, 4, 3, 3, 4)
    eval4 = create_evaluation(group2.id, group1.id, bid4.id, 3, 5, 4, 4, 5)
    eval5 = create_evaluation(group2.id, group3.id, bid5.id, 3, 3, 3, 3, 2)
    eval6 = create_evaluation(group2.id, group1.id, bid6.id, 4, 5, 5, 5, 5)

    # Select some evaluations
    select_evaluation(eval2.id)
    select_evaluation(eval4.id)
    select_evaluation(eval6.id)