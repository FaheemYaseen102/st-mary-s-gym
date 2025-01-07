import csv
from enum import Enum
import tkinter as tk
from tkinter import messagebox, ttk

class MembershipStatus(Enum):
    REGULAR = "Regular"
    PREMIUM = "Premium"
    TRIAL = "Trial"

class GymLocation:
    def __init__(self, location_id, gym_name):
        self.location_id = location_id
        self.gym_name = gym_name
        self.manager = None
        self.workout_zones = []

    def assign_manager(self, manager):
        self.manager = manager

    def add_workout_zone(self, zone):
        self.workout_zones.append(zone)

class GymManager:
    def __init__(self, name, contact):
        self.name = name
        self.contact = contact
        self.workout_zones = []

    def assign_zone(self, zone):
        self.workout_zones.append(zone)

class WorkoutZone:
    def __init__(self, zone_id, zone_name, equipment):
        self.zone_id = zone_id
        self.zone_name = zone_name
        self.equipment = equipment
        self.attendant = None
        self.updates = []  # To store important updates
        self.schedules = []  # To store class schedules
        self.promotions = []  # To store promotions

    def assign_attendant(self, attendant):
        self.attendant = attendant

    def add_update(self, update):
        self.updates.append(update)

    def add_schedule(self, schedule):
        self.schedules.append(schedule)

    def add_promotion(self, promotion):
        self.promotions.append(promotion)

    def get_updates(self):
        return self.updates

    def get_schedules(self):
        return self.schedules

    def get_promotions(self):
        return self.promotions

class Member:
    def __init__(self, member_id, name, health_info):
        self.member_id = member_id
        self.name = name
        self.health_info = health_info
        self.status = MembershipStatus.REGULAR

    def upgrade_membership(self):
        if self.status == MembershipStatus.REGULAR:
            self.status = MembershipStatus.PREMIUM
        elif self.status == MembershipStatus.PREMIUM:
            self.status = MembershipStatus.TRIAL

class Appointment:
    def __init__(self, appointment_id, member, trainer, date_time, service_type):
        self.appointment_id = appointment_id
        self.member = member
        self.trainer = trainer
        self.date_time = date_time
        self.service_type = service_type

class Payment:
    def __init__(self, payment_id, member, amount, payment_method, date):
        self.payment_id = payment_id
        self.member = member
        self.amount = amount
        self.payment_method = payment_method
        self.date = date

class Attendance:
    def __init__(self, attendance_id, member, zone, date_time):
        self.attendance_id = attendance_id
        self.member = member
        self.zone = zone
        self.date_time = date_time

class StaffDashboard:
    def __init__(self, gym_manager):
        self.gym_manager = gym_manager
        self.members = []
        self.appointments = []
        self.payments = []
        self.attendance = []

    def add_member(self, member):
        self.members.append(member)
        self._save_to_csv('members.csv', [member.member_id, member.name, member.health_info, member.status.value])

    def add_appointment(self, appointment):
        self.appointments.append(appointment)
        self._save_to_csv('appointments.csv', [appointment.appointment_id, appointment.member.member_id, appointment.date_time, appointment.service_type])

    def add_payment(self, payment):
        self.payments.append(payment)
        self._save_to_csv('payments.csv', [payment.payment_id, payment.member.member_id, payment.amount, payment.payment_method, payment.date])

    def add_attendance(self, attendance):
        self.attendance.append(attendance)
        self._save_to_csv('attendance.csv', [attendance.attendance_id, attendance.member.member_id, attendance.zone.zone_id, attendance.date_time])

    def _save_to_csv(self, filename, data):
        with open(filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data)

    def generate_reports(self):
        return {
            "Members": len(self.members),
            "Appointments": len(self.appointments),
            "Payments": len(self.payments),
            "Attendance": len(self.attendance),
        }

    def get_members(self):
        return self.members

    def get_appointments(self):
        return self.appointments

    def get_payments(self):
        return self.payments

    def get_attendance(self):
        return self.attendance

class GUI:
    def __init__(self, root, dashboard):
        self.dashboard = dashboard
        self.root = root
        self.root.title("St Mary's Fitness Management")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=1, fill='both')

        self.member_tab = tk.Frame(self.notebook)
        self.notebook.add(self.member_tab, text='Members')

        tk.Label(self.member_tab, text="Add Member").grid(row=0, column=0, columnspan=2)
        tk.Label(self.member_tab, text="ID").grid(row=1, column=0)
        self.member_id_entry = tk.Entry(self.member_tab)
        self.member_id_entry.grid(row=1, column=1)
        tk.Label(self.member_tab, text="Name").grid(row=2, column=0)
        self.member_name_entry = tk.Entry(self.member_tab)
        self.member_name_entry.grid(row=2, column=1)
        tk.Label(self.member_tab, text="Health Info").grid(row=3, column=0)
        self.member_health_entry = tk.Entry(self.member_tab)
        self.member_health_entry.grid(row=3, column=1)
        tk.Button(self.member_tab, text="Add Member", command=self.add_member).grid(row=4, column=0, columnspan=2)

        self.view_members_button = ttk.Button(self.member_tab, text="View Members", command=self.view_members)
        self.view_members_button.grid(row=5, column=0, columnspan=2)

        self.zone_tab = tk.Frame(self.notebook)
        self.notebook.add(self.zone_tab, text='Workout Zones')

        tk.Label(self.zone_tab, text="Add Workout Zone").grid(row=0, column=0, columnspan=2)
        tk.Label(self.zone_tab, text="Zone ID").grid(row=1, column=0)
        self.zone_id_entry = tk.Entry(self.zone_tab)
        self.zone_id_entry.grid(row=1, column=1)
        tk.Label(self.zone_tab, text="Zone Name").grid(row=2, column=0)
        self.zone_name_entry = tk.Entry(self.zone_tab)
        self.zone_name_entry.grid(row=2, column=1)
        tk.Label(self.zone_tab, text="Equipment").grid(row=3, column=0)
        self.zone_equipment_entry = tk.Entry(self.zone_tab)
        self.zone_equipment_entry.grid(row=3, column=1)
        tk.Button(self.zone_tab, text="Add Zone", command=self.add_zone).grid(row=4, column=0, columnspan=2)

        self.view_zones_button = ttk.Button(self.zone_tab, text="View Zones", command=self.view_zones)
        self.view_zones_button.grid(row=5, column=0, columnspan=2)

        self.appointment_tab = tk.Frame(self.notebook)
        self.notebook.add(self.appointment_tab, text='Appointments')

        tk.Label(self.appointment_tab, text="Add Appointment").grid(row=0, column=0, columnspan=2)
        tk.Label(self.appointment_tab, text="ID").grid(row=1, column=0)
        self.appointment_id_entry = tk.Entry(self.appointment_tab)
        self.appointment_id_entry.grid(row=1, column=1)
        tk.Label(self.appointment_tab, text="Member ID").grid(row=2, column=0)
        self.appointment_member_id_entry = tk.Entry(self.appointment_tab)
        self.appointment_member_id_entry.grid(row=2, column=1)
        tk.Label(self.appointment_tab, text="Date & Time").grid(row=3, column=0)
        self.appointment_date_entry = tk.Entry(self.appointment_tab)
        self.appointment_date_entry.grid(row=3, column=1)
        tk.Label(self.appointment_tab, text="Service Type").grid(row=4, column=0)
        self.appointment_service_entry = tk.Entry(self.appointment_tab)
        self.appointment_service_entry.grid(row=4, column=1)
        tk.Button(self.appointment_tab, text="Add Appointment", command=self.add_appointment).grid(row=5, column=0, columnspan=2)

        self.view_appointments_button = ttk.Button(self.appointment_tab, text="View Appointments", command=self.view_appointments)
        self.view_appointments_button.grid(row=6, column=0, columnspan=2)

        self.payment_tab = tk.Frame(self.notebook)
        self.notebook.add(self.payment_tab, text='Payments')

        tk.Label(self.payment_tab, text="Add Payment").grid(row=0, column=0, columnspan=2)
        tk.Label(self.payment_tab, text="ID").grid(row=1, column=0)
        self.payment_id_entry = tk.Entry(self.payment_tab)
        self.payment_id_entry.grid(row=1, column=1)
        tk.Label(self.payment_tab, text="Member ID").grid(row=2, column=0)
        self.payment_member_id_entry = tk.Entry(self.payment_tab)
        self.payment_member_id_entry.grid(row=2, column=1)
        tk.Label(self.payment_tab, text="Amount").grid(row=3, column=0)
        self.payment_amount_entry = tk.Entry(self.payment_tab)
        self.payment_amount_entry.grid(row=3, column=1)
        tk.Label(self.payment_tab, text="Payment Method").grid(row=4, column=0)
        self.payment_method_entry = tk.Entry(self.payment_tab)
        self.payment_method_entry.grid(row=4, column=1)
        tk.Label(self.payment_tab, text="Date").grid(row=5, column=0)
        self.payment_date_entry = tk.Entry(self.payment_tab)
        self.payment_date_entry.grid(row=5, column=1)
        tk.Button(self.payment_tab, text="Add Payment", command=self.add_payment).grid(row=6, column=0, columnspan=2)

        self.view_payments_button = ttk.Button(self.payment_tab, text="View Payments", command=self.view_payments)
        self.view_payments_button.grid(row=7, column=0, columnspan=2)

        self.attendance_tab = tk.Frame(self.notebook)
        self.notebook.add(self.attendance_tab, text='Attendance')

        tk.Label(self.attendance_tab, text="Add Attendance").grid(row=0, column=0, columnspan=2)
        tk.Label(self.attendance_tab, text="ID").grid(row=1, column=0)
        self.attendance_id_entry = tk.Entry(self.attendance_tab)
        self.attendance_id_entry.grid(row=1, column=1)
        tk.Label(self.attendance_tab, text="Member ID").grid(row=2, column=0)
        self.attendance_member_id_entry = tk.Entry(self.attendance_tab)
        self.attendance_member_id_entry.grid(row=2, column=1)
        tk.Label(self.attendance_tab, text="Zone ID").grid(row=3, column=0)
        self.attendance_zone_id_entry = tk.Entry(self.attendance_tab)
        self.attendance_zone_id_entry.grid(row=3, column=1)
        tk.Label(self.attendance_tab, text="Date & Time").grid(row=4, column=0)
        self.attendance_date_entry = tk.Entry(self.attendance_tab)
        self.attendance_date_entry.grid(row=4, column=1)
        tk.Button(self.attendance_tab, text="Add Attendance", command=self.add_attendance).grid(row=5, column=0, columnspan=2)

        self.view_attendance_button = ttk.Button(self.attendance_tab, text="View Attendance", command=self.view_attendance)
        self.view_attendance_button.grid(row=6, column=0, columnspan=2)

        self.report_tab = tk.Frame(self.notebook)
        self.notebook.add(self.report_tab, text='Overall Report')

        tk.Label(self.report_tab, text="Generate Overall Report").grid(row=0, column=0, columnspan=2)
        tk.Label(self.report_tab, text="Select Report Type").grid(row=1, column=0)
        self.report_type = ttk.Combobox(self.report_tab,
                                        values=["Members", "Appointments", "Payments", "Attendance", "Workout Zones"])
        self.report_type.grid(row=1, column=1)
        tk.Button(self.report_tab, text="Generate Report", command=self.generate_report).grid(row=2, column=0,
                                                                                              columnspan=2)

    def add_member(self):
        member_id = self.member_id_entry.get()
        name = self.member_name_entry.get()
        health_info = self.member_health_entry.get()
        member = Member(member_id, name, health_info)
        self.dashboard.add_member(member)
        messagebox.showinfo("Success", f"Member {name} added successfully!")

    def add_zone(self):
        zone_id = self.zone_id_entry.get()
        zone_name = self.zone_name_entry.get()
        equipment = self.zone_equipment_entry.get()
        zone = WorkoutZone(zone_id, zone_name, equipment)
        self.dashboard.gym_manager.assign_zone(zone)
        self.dashboard.gym_manager.workout_zones.append(zone)
        messagebox.showinfo("Success", f"Workout Zone {zone_name} added successfully!")

    def add_appointment(self):
        appointment_id = self.appointment_id_entry.get()
        member_id = self.appointment_member_id_entry.get()
        date_time = self.appointment_date_entry.get()
        service_type = self.appointment_service_entry.get()
        member = next((m for m in self.dashboard.get_members() if m.member_id == member_id), None)
        appointment = Appointment(appointment_id, member, None, date_time, service_type)
        self.dashboard.add_appointment(appointment)
        messagebox.showinfo("Success", f"Appointment {appointment_id} added successfully!")

    def add_payment(self):
        payment_id = self.payment_id_entry.get()
        member_id = self.payment_member_id_entry.get()
        amount = self.payment_amount_entry.get()
        payment_method = self.payment_method_entry.get()
        date = self.payment_date_entry.get()
        member = next((m for m in self.dashboard.get_members() if m.member_id == member_id), None)
        payment = Payment(payment_id, member, amount, payment_method, date)
        self.dashboard.add_payment(payment)
        messagebox.showinfo("Success", f"Payment {payment_id} added successfully!")

    def add_attendance(self):
        attendance_id = self.attendance_id_entry.get()
        member_id = self.attendance_member_id_entry.get()
        zone_id = self.attendance_zone_id_entry.get()
        date_time = self.attendance_date_entry.get()
        member = next((m for m in self.dashboard.get_members() if m.member_id == member_id), None)
        zone = next((z for z in self.dashboard.gym_manager.workout_zones if z.zone_id == zone_id), None)
        attendance = Attendance(attendance_id, member, zone, date_time)
        self.dashboard.add_attendance(attendance)
        messagebox.showinfo("Success", f"Attendance {attendance_id} added successfully!")

    def view_members(self):
        members = self.dashboard.get_members()
        members_info = "\n".join([f"{m.name} ({m.member_id}) - {m.health_info} - {m.status.value}" for m in members])
        messagebox.showinfo("Members", members_info)

    def view_zones(self):
        zones = self.dashboard.gym_manager.workout_zones
        zones_info = "\n".join([f"{z.zone_name} ({z.zone_id}) - {z.equipment}" for z in zones])
        messagebox.showinfo("Workout Zones", zones_info)

    def view_appointments(self):
        appointments = self.dashboard.get_appointments()
        appointments_info = "\n".join([f"{a.date_time} - {a.service_type} (ID: {a.appointment_id})" for a in appointments])
        messagebox.showinfo("Appointments", appointments_info)

    def view_payments(self):
        payments = self.dashboard.get_payments()
        payments_info = "\n".join([f"{p.amount} {p.payment_method} on {p.date} (ID: {p.payment_id})" for p in payments])
        messagebox.showinfo("Payments", payments_info)

    def view_attendance(self):
        attendance = self.dashboard.get_attendance()
        attendance_info = "\n".join([f"{a.date_time} - {a.zone.zone_name} (ID: {a.attendance_id})" for a in attendance])
        messagebox.showinfo("Attendance", attendance_info)

    def generate_report(self):
        report_type = self.report_type.get()
        if report_type == "Members":
            members = self.dashboard.get_members()
            report = "\n".join([f"{m.name} ({m.member_id}) - {m.health_info} - {m.status.value}" for m in members])
        elif report_type == "Appointments":
            appointments = self.dashboard.get_appointments()
            report = "\n".join([f"{a.date_time} - {a.service_type} (ID: {a.appointment_id})" for a in appointments])
        elif report_type == "Payments":
            payments = self.dashboard.get_payments()
            report = "\n".join([f"{p.amount} {p.payment_method} on {p.date} (ID: {p.payment_id})" for p in payments])
        elif report_type == "Attendance":
            attendance = self.dashboard.get_attendance()
            report = "\n".join([f"{a.date_time} - {a.zone.zone_name} (ID: {a.attendance_id})" for a in attendance])
        elif report_type == "Workout Zones":
            zones = self.dashboard.gym_manager.workout_zones
            report = "\n".join([f"{z.zone_name} ({z.zone_id}) - {z.equipment}" for z in zones])
        else:
            report = "Invalid Report Type Selected!"

        messagebox.showinfo("Report", report)

if __name__ == "__main__":
    manager = GymManager("Hammad", "+92 319 5032569")
    gym_location = GymLocation("1", "St Mary's Fitness")
    gym_location.assign_manager(manager)
    staff_dashboard = StaffDashboard(gym_location.manager)
    gui = tk.Tk()
    gui_app = GUI(gui, staff_dashboard)
    gui.mainloop()
