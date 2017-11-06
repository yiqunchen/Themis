import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import xml.etree.ElementTree as ET

import themis2

tree = None

class App(QDialog):
 
    def __init__(self):
        super().__init__()
        self.title = 'Themis 2.0'
        self.left = 100
        self.top = 100
        self.width = 800
        self.height = 1000
        #self.tree = None
        self.dialog = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
 
        self.createThemisGrid()
        
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox4)
        windowLayout.addWidget(self.horizontalGroupBox)
        windowLayout.addWidget(self.horizontalGroupBox2)
        windowLayout.addWidget(self.horizontalGroupBox3)
        self.setLayout(windowLayout)
 
        self.show()

    def createThemisGrid(self):
        self.horizontalGroupBox4 = QGroupBox()
        layout4 = QGridLayout()

        command_box_label = QLabel("Command:")
        self.command_box = QLineEdit(self)

        seed_box_label = QLabel("Random seed:")
        self.seed_box = QLineEdit(self)

        max_box_label = QLabel("Max Samples:")
        self.max_box = QLineEdit(self)

        min_box_label = QLabel("Min Samples:")
        self.min_box = QLineEdit(self)

        layout4.addWidget(command_box_label,1, 0)
        layout4.addWidget(self.command_box,1, 1)

        layout4.addWidget(seed_box_label,2,0)
        layout4.addWidget(self.seed_box,2,1)

        layout4.addWidget(max_box_label,3,0)
        layout4.addWidget(self.max_box,3,1)

        layout4.addWidget(min_box_label,4,0)
        layout4.addWidget(self.min_box,4,1)

        self.horizontalGroupBox = QGroupBox("Inputs")
        self.horizontalGroupBox.setFont(QFont("", pointSize=14))
        layout = QGridLayout()
        layout.setSpacing(5)

        self.createInputsTable()

        #inputs_table.selectedItems()
        #inputs_table.selectedRanges()

        
        add_button = QPushButton('Add Input...')
        add_button.setAutoDefault(False)

        add_button.clicked.connect(self.handleAddButton)

        layout.addWidget(self.inputs_table,0,1, 3, 4)
        layout.addWidget(add_button,5,1)

        self.horizontalGroupBox2 = QGroupBox("Tests")
        self.horizontalGroupBox2.setFont(QFont("", pointSize=14))
        
        layout2 = QGridLayout()
        
        self.createTestsTable()

        add_test_button = QPushButton("Add Test...")
        add_test_button.setAutoDefault(False)

        layout2.addWidget(self.tests_table, 5, 4, 4, 4)
        layout2.addWidget(add_test_button, 9, 4)


        self.horizontalGroupBox3 = QGroupBox("")
        self.layout3 = QGridLayout()

        self.results_box = QTextEdit()
        self.results_box.setReadOnly(True)

        run_button = QPushButton("Run")
        run_button.clicked.connect(self.handleRunButton)

        load_button = QPushButton('Load...')
        load_button.setDefault(True)
        
        save_button = QPushButton('Save...')


        save_button.clicked.connect(self.handleSaveButton)
        add_test_button.clicked.connect(self.handleAddButton)
        load_button.clicked.connect(self.handleLoadButton)

        self.layout3.addWidget(load_button,1, 1)
        self.layout3.addWidget(save_button,1, 2)
        
        self.layout3.addWidget(run_button,1, 3)
        self.layout3.addWidget(self.results_box, 2, 1, 5, 5)        

        self.horizontalGroupBox3.setLayout(self.layout3)
        self.horizontalGroupBox.setLayout(layout)
        self.horizontalGroupBox2.setLayout(layout2)
        
        self.horizontalGroupBox4.setLayout(layout4)

    def handleRunButton(self):

        self.tester.run()

        self.results_box.setText("<h1 style=\"text-align:center\">Themis 2.0 Execution Complete!</h1>");

        if self.tester.group_tests:
            self.results_box.append("<h2> Group Discrimination </h2>")
            self.results_box.append("<p> Your software discriminates with respect to characteristics of the following inputs: <br></p>")
##            self.results_box.append("<ul>")

 
##            for key, value in self.tester.group_tests.items():
                
                

##            self.results_box.append("</ul>")
            
        if self.tester.causal_tests:
            self.results_box.append("<h2> Causal Discrimination </h2>")
            self.results_box.append("<p> Your software discriminates against individuals based on characteristics of the following inputs (given other input characteristics are fixed): <br></p>")
##            self.results_box.append("<ul>")


##            self.results_box.append("</ul>")
        for test in self.tester.tests:
            if test.group == True or test.causal == True:
                self.results_box.append("<h2> Discrimination Search </h2>")
                if test.group == True:
                    self.results_box.append("<h3> Group Discrimination Search </h3>")
                if test.causal == True:
                    self.results_box.append("<h3> Causal Discrimination Search </h3>")
            

        # use flags to determine what to show
        # make sure Themis saving everything needed for summary

        self.results_box.toHtml()

        detailed_output_btn = QPushButton("More details...")
        self.layout3.addWidget(detailed_output_btn, 8, 4)

        detailed_output_btn.clicked.connect(self.handleDetailedButton)

        self.horizontalGroupBox3.setLayout(self.layout3)

    def handleDetailedButton(self):
        dialog = QDialog()

        horizontalGroupBox = QGroupBox("Detailed Discrimination Findings")
        horizontalGroupBox.setFont(QFont("", pointSize=14))
        layout = QGridLayout()
        
        detailed_output_box = QTextEdit()
        detailed_output_box.setReadOnly(True)
        detailed_output_box.setText("")

        if self.tester.group_tests:
            detailed_output_box.append("<h2>Group Discrimination Tests</h2>")
        if self.tester.causal_tests:
            detailed_output_box.append("<h2>Causal Discrimination Tests</h2>")
        for test in self.tester.tests:
            if test.group == True or test.causal == True:
                detailed_output_box.append("<h2>Discrimination Search Results</h2>")
                if test.group == True:
                    self.results_box.append("<h3> Group Discrimination Search </h3>")
                if test.causal == True:
                    self.results_box.append("<h3> Causal Discrimination Search </h3>")

        detailed_output_box.toHtml()

        layout.addWidget(detailed_output_box, 1, 1, 5, 5)
        horizontalGroupBox.setLayout(layout)

        dialog.setGeometry(self.left, self.top, self.width, self.height)

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(horizontalGroupBox)
        dialog.setLayout(windowLayout)

        dialog.setWindowTitle("Themis 2.0: Detailed Output")
        dialog.exec_()

        

        # create button for detailed output

        # traverse tester.group_tests, causal_tests

        # check tests for discrim search -- separate group and causal results for printing
        
##        self.results_box.setText(self.tester.output)

    def handleAddButton(self):

        return
##        if table is self.tests_table:
##            self.dialog = EditTestWindow()
##            self.dialog.setModal(True)
##            self.dialog.show()
##
##        else:
##            self.dialog = EditInputWindow()
##            self.dialog.setModal(True)
##            self.dialog.show()

    def handleLoadButton(self):
        dialog = QFileDialog()
        filename = dialog.getOpenFileName(self, "Open File", "/home")

        if filename[0]:
            self.file = open(filename[0], 'r')
        else:
            return

        self.tester = themis2.Themis(filename[0])

        command =  self.tester.command
        rand_seed = self.tester.rand_seed
        max_samples = self.tester.max_samples
        min_samples = self.tester.min_samples
        
        # set text boxes from Themis
        self.command_box.setText(str(command))
        self.seed_box.setText(str(rand_seed))
        self.max_box.setText(str(max_samples))
        self.min_box.setText(str(min_samples))

        # input names from tests, input = Themis.inputs[name]; for value in input.values

        index = 0
        inputs = []
        for test in self.tester.tests:
            self.tests_table.insertRow(index)
            self.createEditButtons(self.tests_table,index, test)
            
            function = test.function
            confidence = test.conf
            margin = test.margin

            self.setTestTableValue(str(function),index,1)
            self.setTestTableValue(str(confidence), index, 2)
            self.setTestTableValue(str(margin), index, 3)

            index += 1

            for field in test.i_fields:
                if field not in inputs:
                    inputs.append(field)
            

        self.resizeCells(self.tests_table) 
        
        i = 0
        for name in self.tester.input_names:
            self.inputs_table.insertRow(i)
            self.createEditButtons(self.inputs_table, i, test)
            
            inpt = self.tester.inputs[name]
            
            name = inpt.name
            inpt_type = inpt.kind
            values = inpt.values

            self.setCellValue(name, i, 1)
            self.setCellValue(inpt_type, i, 2)

            if inpt_type == "categorical":
                value = "{" + ", ".join(values) + "}"
                self.setCellValue(value, i, 3)
            else:
                value = "[" + inpt.lb + "-" + inpt.ub + "]"
                self.setCellValue(value, i, 3)
                    
            i +=1

        self.resizeCells(self.inputs_table)

    def resizeCells(self, table):
        
        table.resizeRowsToContents()
 
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setStretchLastSection(True)

        for i in range(table.rowCount()-1):
            table.resizeColumnToContents(i)      

            
            
    def handleSaveButton(self):

        return
        
    def createInputsTable(self):        
        
        self.inputs_table = QTableWidget()
        self.inputs_table.setColumnCount(4)
        self.inputs_table.setHorizontalHeaderLabels(["", "Input Name", "Input Type", "Values"])
        self.inputs_table.horizontalHeader().setStretchLastSection(True)

        self.resizeCells(self.inputs_table)

    def createTestsTable(self):
        self.tests_table = QTableWidget()
        self.tests_table.setColumnCount(5)
        self.tests_table.setHorizontalHeaderLabels(["", "Name", "Confidence", "Margin", "Notes"])
       
        self.resizeCells(self.tests_table)
        
    def createEditButtons(self, table, row, test):
        layout = QHBoxLayout()
        layout.setContentsMargins(2,2,2,2)
        layout.setSpacing(10)
        
        delete_btn = QPushButton(table)
        delete_btn.setText("Delete")
        delete_btn.adjustSize()
        layout.addWidget(delete_btn)

        edit_btn = QPushButton(table)
        edit_btn.setText("Edit...")
        
        index = QPersistentModelIndex(table.model().index(row, 0))
        
        edit_btn.clicked.connect(lambda *args, index=index: self.handleEditButton(index, table, test))
        
        layout.addWidget(edit_btn)
        
        cellWidget = QWidget()
        cellWidget.setLayout(layout)
        
        table.setCellWidget(row,0,cellWidget)
        
    def handleEditButton(self, index, table, test):

        if table is self.inputs_table:
            item_name = table.item(index.row(), 1)
            item_type = table.item(index.row(), 2)
            item_values = table.item(index.row(), 3)
            print ("Name: " + item_name.text())
            print ("Type: " + item_type.text())
            print ("Values :" + item_values.text())
            
            edit_input_dialog = EditInputWindow(item_name.text(), item_type.text(), item_values.text())
            edit_input_dialog.setModal(True)
            edit_input_dialog.show()

        if table is self.tests_table:
            test_name = table.item(index.row(), 1)
            confidence = table.item(index.row(), 2)
            margin = table.item(index.row(), 3)
            
            self.edit_test_dialog = EditTestWindow(test_name.text(), confidence.text(), margin.text(), test)
            self.edit_test_dialog.setModal(True)
            self.edit_test_dialog.show()

        self.updateTable(table, index)
            
    def updateTable(self, table, index):
        if self.edit_test_dialog.exec_():
            if table is self.tests_table:
                test = self.tester.tests[index.row()]
                
                #update Themis values
                if self.edit_test_dialog.group_cb.isChecked():
                    test.function = "group_discrimination"
                    table.item(index.row(),1,).setText("group_discrimination")
                elif self.edit_test_dialog.causal_cb.isChecked():
                    table.item(index.row(),1).setText("causal_discrimination")
                    test.function = "causal_discrimination"
                elif self.edit_test_dialog.discrim_causal_cb.isChecked() or self.edit_test_dialog.discrim_group_cb.isChecked():
                    table.item(index.row(),1).setText("discrimination_search")
                    test.function = "discrimination_search"
                    if self.edit_test_dialog.discrim_causal_cb.isChecked() and not self.edit_test_dialog.discrim_group_cb.isChecked():
                        test.group = False
                        test.causal = True
                    elif not self.edit_test_dialog.discrim_causal_cb.isChecked() and self.edit_test_dialog.discrim_group_cb.isChecked():
                        test.group = True
                        test.causal = False
                    else:
                        test.group = True
                        test.causal = True

                test.conf = float(self.edit_test_dialog.conf_box.text())
                table.item(index.row(), 2).setText(str(test.conf))
                
                test.margin = float(self.edit_test_dialog.margin_box.text())
                table.item(index.row(), 3).setText(str(test.margin))

                self.tester.tests[index.row()] = test
                
##         elif self.edit_input_dialog.exec_():
##             return
                
                
##            print (test.group)
##            print (test.causal)
##            print (test.conf)
##            print (test.margin)
##            print ("Test modified!")


    def setCellValue(self, value, row, column):
        new_input = QTableWidgetItem()
        new_input.setText(value)
        self.inputs_table.setItem(row,column,new_input)

    def setTestTableValue(self, value, row, column):
        new_input = QTableWidgetItem()
        new_input.setText(value)
        self.tests_table.setItem(row,column,new_input)
        

class EditTestWindow(QDialog):
    def __init__(self, name=None, conf=None, margin=None, test=None):
        super().__init__()
        self.title = 'Add or Edit Tests'
        self.left = 100
        self.top = 100
        self.width = 500
        self.height = 300

        if name == None and conf == None and margin == None and test==None: 
            self.initUI()
        else:
            self.initUI(name, conf, margin, test)

    def initUI(self, name=None, conf=None, margin=None, test=None):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        if name == None and conf == None and margin == None and test==None:
            self.createGrid()
        else:
            self.createGrid(name, conf, margin, test)
            
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)

    ##        self.show()

    def createGrid(self, name=None, conf=None, margin=None, test=None):
        self.horizontalGroupBox = QGroupBox("")
        layout = QGridLayout()

        self.type_label = QLabel("Test Function Name: ")
        self.group_cb = QCheckBox('Group Discrimination',self)
        self.causal_cb = QCheckBox('Causal Discrimination',self)
        self.discrim_causal_cb = QCheckBox('Discrimination Search (Causal)',self)
        self.discrim_group_cb = QCheckBox('Discrimination Search (Group)',self)

        if name is not None:
            if name == "group_discrimination":
                self.group_cb.setChecked(True)
            elif name == "causal_discrimination":
                self.causal_cb.setChecked(True)
            elif name == "discrimination_search":
                if test is not None:
                    if test.group == True:
                        self.discrim_group_cb.setChecked(True)
                    if test.causal == True:
                        self.discrim_causal_cb.setChecked(True)
                else:
                    print ("No test was passed in!")
                

        self.group_cb.stateChanged.connect(self.selectionChange)
        self.causal_cb.stateChanged.connect(self.selectionChange)
        self.discrim_group_cb.stateChanged.connect(self.selectionChange)
        self.discrim_causal_cb.stateChanged.connect(self.selectionChange)

        layout.addWidget(self.type_label, 1, 1)
        layout.addWidget(self.group_cb, 1, 2)
        layout.addWidget(self.causal_cb, 2, 2)
        layout.addWidget(self.discrim_group_cb, 3, 2)
        layout.addWidget(self.discrim_causal_cb, 4, 2)

        self.conf_label = QLabel("Enter confidence value: ")
        self.conf_box = QLineEdit(self)

        if conf is not None:
            self.conf_box.setText(str(conf))

        layout.addWidget(self.conf_label, 5, 1)
        layout.addWidget(self.conf_box, 5, 2)

        self.margin_label = QLabel("Enter margin (should add to confidence to make 1.0): ")
        self.margin_box = QLineEdit(self)

        if margin is not None:
            self.margin_box.setText(str(margin))

        layout.addWidget(self.margin_label, 6, 1)
        layout.addWidget(self.margin_box, 6, 2)

        #self.add_button = QPushButton("Add")

        #self.layout.addWidget(self.add_button, 4, 1)

        self.done_button = QPushButton("Done")
        self.done_button.clicked.connect(self.handleDoneButton)

        layout.addWidget(self.done_button, 7, 4)

        self.horizontalGroupBox.setLayout(layout)

    def selectionChange(self):

        return

    def handleDoneButton(self):
        self.accept()


    
class EditInputWindow(QDialog):

    def __init__(self, name=None, kind="categorical", values=None):
        super().__init__()
        self.title = 'Add or Edit Inputs'
        self.left = 100
        self.top = 100
        self.width = 500
        self.height = 300
##        self.v = var
        if name == None and kind == "categorical" and values == None: 
            self.initUI()
        else:
            self.initUI(name, kind, values)


    def initUI(self, name=None, kind="categorical",values=None):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        if name == None and kind == "categorical" and values == None:
            self.createGrid()
        else:
            self.createGrid(name, kind, values)

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)

    def createGrid(self, name=None, kind="categorical", values=None):
        self.horizontalGroupBox = QGroupBox("")
        layout = QGridLayout()

        name_label = QLabel("Input name: ")
        self.name_box = QLineEdit(self)

        if name is not None:
            self.name_box.setText(str(name))

        layout.addWidget(name_label, 1, 1)
        layout.addWidget(self.name_box, 1, 2)

        self.type_label = QLabel("Input type: ")
        self.types = QComboBox()
        self.types.addItem("Categorical")
        self.types.addItem("Continuous Int")

        if kind == "continuousInt":
            index = self.types.findText("Continuous Int")
            if index >= 0:
                self.types.setCurrentIndex(index)
            else:
                print ("Can't find item in combo box!")
        

        layout.addWidget(self.type_label, 2, 1)
        layout.addWidget(self.types, 2, 2)
        self.values_label = QLabel("Values (separated by commas): ")
        self.values_box = QLineEdit(self)

        if values is not None:
            self.values_box.setText(values)
            
            
        layout.addWidget(self.values_label, 3, 1)
        layout.addWidget(self.values_box, 3, 2)
        
        self.types.currentIndexChanged.connect(self.selectionChange)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.handleAddButton)
        layout.addWidget(self.add_button, 4, 1)

        self.done_button = QPushButton("Done")
        self.done_button.clicked.connect(self.handleDoneButton)

        layout.addWidget(self.done_button, 4, 4)
        
        self.horizontalGroupBox.setLayout(layout)
        #print(self.name_box.text())

    def selectionChange(self):

        if self.types.currentText() == "Continuous Int":
            self.values_label.setText("Enter range (e.g. 1-10) : ")
        else:
            self.values_label.setText("Values (separated by commas): ")

    def handleAddButton(self):
        print(self.name_box.text())
        print(self.values_box.text())
        print(self.types.currentText())
        

    def handleDoneButton(self):
        
        self.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
