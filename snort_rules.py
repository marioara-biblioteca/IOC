import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QCheckBox
from PyQt5.QtCore import Qt

class SnortRuleForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Snort Rule Form')
        self.create_top_form()
        
         # Create a layout and add widgets
        

    def create_top_form(self):
        # Create labels and input fields
        rule_id_label = QLabel('Rule ID:')
        self.rule_id_input = QLineEdit()

        # create combobox
        protocol_label = QLabel('Protocol:')
        self.protocol_combo = QComboBox()
        self.protocol_combo.addItem('TCP')
        self.protocol_combo.addItem('UDP')
        self.protocol_combo.addItem('ICMP')


        # Forms for IPs configuration
        source_ip_label = QLabel('Source IP:')
        self.source_ip_input = QLineEdit()
        source_port_label = QLabel('Source Port:')  
        self.source_port_input = QLineEdit()

        dest_ip_label = QLabel('Destination IP:')
        self.dest_ip_input = QLineEdit()
        dest_port_label = QLabel('Destination Port:')
        self.dest_port_input = QLineEdit()
    
        action_label = QLabel('Action:')
        self.action_input = QLineEdit()

        message_text_label = QLabel("Message text:")
        self.message_text_input = QLineEdit()

        class_type_label = QLabel("Class-Type:")
        self.class_type_input = QLineEdit()

        priority_label = QLabel("Priority:")
        self.priority_input = QLineEdit()

        gid_label = QLabel("GID:")
        self.gid_input = QLineEdit()

        # Create a submit button
        submit_button = QPushButton('Submit')
        submit_button.clicked.connect(self.submit)

        # Create a layout and add widgets
        layout = QVBoxLayout()

        # Define horizontal layout for top form
        form_layout = QHBoxLayout()
        form_layout.addWidget(rule_id_label)
        form_layout.addWidget(self.rule_id_input)
        form_layout.addWidget(protocol_label)
        form_layout.addWidget(self.protocol_combo)
        form_layout.addWidget(source_ip_label)
        form_layout.addWidget(self.source_ip_input)
        form_layout.addWidget(source_port_label)
        form_layout.addWidget(self.source_port_input)
        form_layout.addWidget(dest_ip_label)
        form_layout.addWidget(self.dest_ip_input)
        form_layout.addWidget(dest_port_label)
        form_layout.addWidget(self.dest_port_input)
        form_layout.addWidget(action_label)
        form_layout.addWidget(self.action_input)

        layout.addLayout(form_layout)

        # Define second Horizontal layout
        second_row_layout = QHBoxLayout()
        second_row_layout.addWidget(message_text_label)
        second_row_layout.addWidget(self.message_text_input)
        second_row_layout.addWidget(class_type_label)
        second_row_layout.addWidget(self.class_type_input)
        second_row_layout.addWidget(priority_label)
        second_row_layout.addWidget(self.priority_input)
        second_row_layout.addWidget(gid_label)
        second_row_layout.addWidget(self.gid_input)

        layout.addLayout(second_row_layout)

        tcp_layout = QVBoxLayout()
        tcp_label = QLabel("TCP: ")
        tcp_layout.addWidget(tcp_label)
        layout.addLayout(tcp_layout)


        HTTP_layout = QHBoxLayout()
        HTTP_method = QLabel("HTTP Method")
        self.method_combo = QComboBox()
        self.method_combo.addItem('POST')
        self.method_combo.addItem('GET')
        self.method_combo.addItem('PUT')

        HTTP_status_code = QLabel("HTTP Status Code")
        self.status_code_combo = QComboBox()
        self.status_code_combo.addItem('200')
        self.status_code_combo.addItem('404')
        self.status_code_combo.addItem('403')
        
        HTTP_layout.addWidget(HTTP_method,alignment=Qt.AlignmentFlag.AlignAbsolute)
        HTTP_layout.addWidget(self.method_combo)
        HTTP_layout.addWidget(HTTP_status_code, alignment=Qt.AlignmentFlag.AlignAbsolute)
        HTTP_layout.addWidget(self.status_code_combo)

        TCP_flags_layout = QHBoxLayout()

        TCP_flags_label = QLabel("TCP Flags")
        TCP_flags_layout.addWidget(TCP_flags_label)

        self.checkbox_ack = QCheckBox("ACK")
        self.checkbox_ack.stateChanged.connect(lambda:self.btnstate(self.checkbox_ack))
        TCP_flags_layout.addWidget(self.checkbox_ack, alignment=Qt.AlignmentFlag.AlignLeft)


        self.checkbox_syn = QCheckBox("SYN")
        self.checkbox_syn.stateChanged.connect(lambda:self.btnstate(self.checkbox_syn))
        TCP_flags_layout.addWidget(self.checkbox_syn, alignment=Qt.AlignmentFlag.AlignLeft)

        self.checkbox_psh = QCheckBox("PSH")
        self.checkbox_psh.stateChanged.connect(lambda:self.btnstate(self.checkbox_psh))
        TCP_flags_layout.addWidget(self.checkbox_psh)


        self.checkbox_rst = QCheckBox("RST")
        self.checkbox_rst.stateChanged.connect(lambda:self.btnstate(self.checkbox_rst))
        TCP_flags_layout.addWidget(self.checkbox_rst)

        self.checkbox_fin = QCheckBox("FIN")
        self.checkbox_fin.stateChanged.connect(lambda:self.btnstate(self.checkbox_fin))
        TCP_flags_layout.addWidget(self.checkbox_fin)


        layout.addLayout(HTTP_layout)
        layout.addLayout(TCP_flags_layout)
        #layout.addLayout(HTTP_status_code)
        
        

        layout.addWidget(submit_button)

        self.setLayout(layout)
        self.show()


    def btnstate(self, b):
        return b.isChecked()

    def submit(self):
        rule_id = self.rule_id_input.text()
        protocol = self.protocol_combo.currentText()
        source_ip = self.source_ip_input.text()
        source_port = self.source_port_input.text()
        dest_ip = self.dest_ip_input.text()
        dest_port = self.dest_port_input.text()
        action = self.action_input

        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = SnortRuleForm()
    sys.exit(app.exec_())