<template>
  <div>
    <el-container>
      <!--    SideBar  -->
      <el-aside :width="asideWidth" style="min-height: 100vh; background-color: #001529">
        <div style="
                                height: 60px;
                                color: white;
                                display: flex;
                                align-items: center;
                                justify-content: center;
                              ">
          <img src="@/assets/UCS-Logo.png" alt="" style="width: 120px; height: 60px" />
        </div>

        <el-menu :collapse="isCollapse" :collapse-transition="false" router background-color="#001529"
          text-color="rgba(255, 255, 255, 0.65)" active-text-color="#fff" style="border: none"
          :default-active="$route.path">
          <el-menu-item index="/">
            <i class="el-icon-house"></i>
            <span slot="title">Home Page</span>
          </el-menu-item>
          <el-menu-item index="/edit">
            <i class="el-icon-time"></i>
            <span slot="title">Edit History</span>
          </el-menu-item>
          <el-menu-item index="/removed">
            <i class="el-icon-delete"></i>
            <span slot="title">Removed</span>
          </el-menu-item>
          <el-menu-item index="/history">
            <i class="el-icon-time"></i>
            <span slot="title">History</span>
          </el-menu-item>
          <el-menu-item @click="logout">
            <i class="el-icon-switch-button"></i>
            <span slot="title">Logout</span>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <el-container>
        <!--        Header-->
        <el-header>
          <!--          <i :class="collapseIcon" style="font-size: 26px" @click="handleCollapse"></i>-->
          <el-breadcrumb style="margin-left: 20px">
            <el-breadcrumb-item>Welcome, {{ username }}!</el-breadcrumb-item>
          </el-breadcrumb>

          <el-breadcrumb separator-class="el-icon-arrow-right" style="margin-left: 20px">
            <el-breadcrumb-item>Home Page</el-breadcrumb-item>
          </el-breadcrumb>



          <!-- Search input for satellite name -->
          <el-input v-model="searchQuery" placeholder="Search by Satellite Name"
            style="width: 300px; margin-left: 20px; margin-right: 20px;">
          </el-input>

          Remove: <el-switch v-model="showRemoveColumn" style="margin-left: 10px; margin-right: 10px;" />

          <el-dropdown>
            <el-button>
              Filter Column<i class="el-icon-arrow-down el-icon--right"></i>
            </el-button>
            <el-dropdown-menu slot="dropdown">
              <el-checkbox-group v-model="selectedColumns">
                <el-checkbox label="un_registry_country">UN Registry Country</el-checkbox>
                <el-checkbox label="operator_country">Operator Country</el-checkbox>
                <el-checkbox label="operator">operator</el-checkbox>
                <!-- Repeat for other columns -->
              </el-checkbox-group>
            </el-dropdown-menu>
          </el-dropdown>


        </el-header>

        <!--        Main Page-->
        <el-main>


          <el-table :data="filteredData" border style="width: 100%" :row-style="
            ({ row }) =>
              row.data_status === 1 ? { backgroundColor: '#ffe79f' } : {}
          ">
            <el-table-column fixed prop="satellite_name" label="satellite_name">
              <!-- copy v-if to filter column -->
            </el-table-column>
            <el-table-column prop="un_registry_country" label="un_registry_country" :filters="[
              { text: 'Country11', value: 'Country11' },
              { text: 'Country12', value: 'Country12' },
              { text: 'Country13', value: 'Country13' },
              { text: 'Country14', value: 'Country14' },]" :filter-method="filterHandler"
              filter-placement="bottom-start" v-if="selectedColumns.includes('un_registry_country')">
              <!-- copy template to if want edit function -->
              <template slot-scope="scope">
                <!-- Check if the row is not in editing mode -->
                <div v-if="!scope.row.editing">{{ scope.row.un_registry_country }}</div>
                <!-- If the row is in editing mode, show the input with tooltip -->
                <el-tooltip v-else class="item" effect="dark" :content="scope.row.un_registry_country"
                  placement="top-start">
                  <el-input v-model="scope.row.un_registry_country" size="mini"></el-input>
                </el-tooltip>
              </template>
            </el-table-column>
            <el-table-column prop="operator_country" label="operator_country"
              v-if="selectedColumns.includes('operator_country')">
              <template slot-scope="scope">
                <div v-if="!scope.row.editing">{{ scope.row.operator_country }}</div>
                <el-tooltip v-else class="item" effect="dark" :content="scope.row.operator_country" placement="top-start">
                  <el-input v-model="scope.row.operator_country" size="mini"></el-input>
                </el-tooltip>
              </template>
            </el-table-column>
            <el-table-column prop="operator" label="operator" v-if="selectedColumns.includes('operator')">
              <template slot-scope="scope">
                <div v-if="!scope.row.editing">{{ scope.row.operator }}</div>
                <el-tooltip v-else class="item" effect="dark" :content="scope.row.operator" placement="top-start">
                  <el-input v-model="scope.row.operator" size="mini"></el-input>
                </el-tooltip>
              </template>
            </el-table-column>
            <el-table-column prop="user_type" label="user_type" width="120">
              <template slot-scope="scope">
                <div v-if="!scope.row.editing">{{ scope.row.user_type }}</div>
                <el-tooltip v-else class="item" effect="dark" :content="scope.row.user_type" placement="top-start">
                  <el-input v-model="scope.row.user_type" size="mini"></el-input>
                </el-tooltip>
              </template>
            </el-table-column>
            <el-table-column prop="purpose" label="purpose">
              <template slot-scope="scope">
                <div v-if="!scope.row.editing">{{ scope.row.purpose }}</div>
                <el-tooltip v-else class="item" effect="dark" :content="scope.row.purpose" placement="top-start">
                  <el-input v-model="scope.row.purpose" size="mini"></el-input>
                </el-tooltip>
              </template>
            </el-table-column>
            <el-table-column prop="detailed_purpose" label="detailed_purpose">
              <template slot-scope="scope">
                <div v-if="!scope.row.editing">{{ scope.row.detailed_purpose }}</div>
                <el-tooltip v-else class="item" effect="dark" :content="scope.row.detailed_purpose" placement="top-start">
                  <el-input v-model="scope.row.detailed_purpose" size="mini"></el-input>
                </el-tooltip>
              </template>
            </el-table-column>
            <el-table-column prop="orbit_class" label="orbit_class">
              <template slot-scope="scope">
                <div v-if="!scope.row.editing">{{ scope.row.orbit_class }}</div>
                <el-tooltip v-else class="item" effect="dark" :content="scope.row.orbit_class" placement="top-start">
                  <el-input v-model="scope.row.orbit_class" size="mini"></el-input>
                </el-tooltip>
              </template>
            </el-table-column>
            <el-table-column prop="orbit_type" label="orbit_type" width="120">
              <template slot-scope="scope">
                <div v-if="!scope.row.editing">
                  {{ scope.row.orbit_type }}
                </div>
                <el-tooltip v-else class="item" effect="dark" :content="scope.row.orbit_type" placement="top-start">
                  <el-input v-model="scope.row.orbit_type" size="mini"></el-input>
                </el-tooltip>
              </template>
            </el-table-column>
            <el-table-column prop="longitude_geo" label="longitude_geo">
              <template slot-scope="scope">
                <div v-if="!scope.row.editing">{{ scope.row.longitude_geo }}</div>
                <el-tooltip v-else class="item" effect="dark" :content="scope.row.longitude_geo" placement="top-start">
                  <el-input v-model="scope.row.longitude_geo" size="mini"></el-input>
                </el-tooltip>
              </template>
            </el-table-column>
            <el-table-column prop="perigee" label="perigee"></el-table-column>
            <el-table-column prop="apogee" label="apogee" width="150"></el-table-column>
            <el-table-column prop="eccentricity" label="eccentricity" width="150"></el-table-column>
            <el-table-column prop="inclination" label="inclination" width="150"></el-table-column>
            <el-table-column prop="orbital_period" label="orbital_period" width="150"></el-table-column>
            <el-table-column prop="launch_mass" label="launch_mass" width="150"></el-table-column>
            <el-table-column prop="dry_mass" label="dry_mass" width="150"></el-table-column>
            <el-table-column prop="power" label="power" width="150"></el-table-column>
            <el-table-column prop="launch_date" label="launch_date" width="150"></el-table-column>
            <el-table-column prop="lifetime" label="lifetime" width="150"></el-table-column>
            <el-table-column prop="contractor" label="contractor" width="150"></el-table-column>
            <el-table-column prop="contractor_country" label="contractor_country" width="150"></el-table-column>
            <el-table-column prop="launch_site" label="launch_site" width="150"></el-table-column>
            <el-table-column prop="launch_vehicle" label="launch_vehicle" width="150"></el-table-column>
            <el-table-column prop="cospar" label="cospar" width="150"></el-table-column>
            <el-table-column prop="norad" label="norad" width="150"></el-table-column>
            <el-table-column prop="comments" label="comments" width="150"></el-table-column>
            <el-table-column prop="orbital_data_source" label="orbital_data_source" width="150"></el-table-column>
            <el-table-column prop="source1" label="source1" width="150"></el-table-column>
            <el-table-column prop="data_status" label="data_status" width="150"></el-table-column>
            <el-table-column fixed="right" label="Edit">
              <template slot-scope="scope">
                <el-button v-if="!scope.row.editing" size="mini" class="operation-button"
                  @click="startEdit(scope.row)">Edit
                </el-button>
                <el-button v-if="scope.row.editing" size="mini" class="operation-button" @click="saveEdit(scope.row)">Save
                </el-button>
                <el-button v-if="scope.row.editing" size="mini" class="operation-button"
                  @click="cancelEdit(scope.row)">Cancel
                </el-button>
              </template>
            </el-table-column>
            <!-- New Remove Column -->
            <el-table-column fixed="right" label="Remove" width="100" v-if="showRemoveColumn">
              <template slot-scope="scope">
                <el-button type="danger" size="mini" @click="handleRemoveRow(scope.row)">Remove</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-main>

        <el-dialog title="Select a Reason for Removal" :visible.sync="isRemoveModalVisible" width="30%">
          <el-radio-group v-model="selectedOption">
            <el-radio label="Re-entered">Re-entered</el-radio>
            <el-radio label="Non-operational">Non-operational</el-radio>
            <el-radio label="Others">Others</el-radio>
          </el-radio-group>

          <el-input v-if="selectedOption === 'Others'" v-model="otherReason"
            placeholder="Please specify the reason"></el-input>

          <span slot="footer" class="dialog-footer">
            <el-button @click="isRemoveModalVisible = false">Cancel</el-button>
            <el-button type="primary" @click="confirmRemoval">Confirm</el-button>
          </span>
        </el-dialog>

      </el-container>
    </el-container>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      isCollapse: false,
      asideWidth: "200px",
      collapseIcon: "el-icon-s-fold",
      tableData: [],
      editDialogVisible: false,
      backupRow: null,
      filtersActive: false,
      // TODO put all columns in selectedColumns  expect pk  
      selectedColumns: ['un_registry_country', 'operator_country', 'operator'],
      searchQuery: '',
      username: '',
      showRemoveColumn: false,
      isRemoveModalVisible: false,
      selectedOption: '',
      otherReason: '',
    };
  },
  mounted() {
    this.fetchSatellites();
    this.getUsername();
  },
  methods: {
    handleRemoveRow(row) {
      this.currentRow = row; // Store the current row for further processing
      this.isRemoveModalVisible = true; // Show the modal
    },
    confirmRemoval() {
      // Construct the payload to be sent
      const payload = {
        cospar: this.currentRow.cospar, // Assuming 'satellite_name' is the identifier
        reason: this.selectedOption === 'Others' ? this.otherReason : this.selectedOption,
      };

      console.log(payload)

          
      // Send an AJAX request
      axios.post('http://localhost:8000/api/remove-sat', payload)
        .then(response => {
          // Handle success response
          console.log('Data sent successfully:', response);

          // Remove the row from the local data, if needed
          const index = this.tableData.indexOf(this.currentRow);
          if (index > -1) {
            this.tableData.splice(index, 1);
          }
        })
        .catch(error => {
          // Handle error response
          console.error('Error sending data:', error);
        });

      // Reset modal state and hide it
      this.isRemoveModalVisible = false;
      this.selectedOption = '';
      this.otherReason = '';
    },
    logout() {
      localStorage.removeItem('authToken'); // 清除本地存储中的 token
      this.$router.push('/login'); // 重定向到登录页面
    },
    getUsername() {
      // Retrieve the username from local storage
      this.username = localStorage.getItem('username');
      console.log("Retrieved username:", this.username);
    },
    async fetchSatellites() {
      try {
        const response = await axios.get(
          "http://localhost:8000/api/satellites"
        ); // replace with your Flask app URL
        this.tableData = response.data.map((row) => ({
          ...row,
          editing: false,
        }));
        console.log(this.tableData);
      } catch (error) {
        console.error("There was an error fetching the data:", error);
      }
    },
    removeRow(index, row) {
      this.tableData.splice(index, 1); // Remove the row
      // You may also want to delete the row from your backend/database
    },
    tableRowClassName({ row, rowIndex }) {
      // Here, you can specify a condition to highlight rows that need attention
      if (rowIndex === 2) {
        return "highlight-row";
      }
      return "";
    },
    startEdit(row) {
      // Backup the original data
      this.backupRow = Object.assign({}, row);
      this.tableData.forEach((r) => {
        r.editing = false;
      }); // Ensure only one row is in edit mode
      row.editing = true;
    },
    saveEdit(row) {
      let edit_records = [];
      // Collect changes, excluding the 'editing' property
      for (const key in row) {
        if (key !== 'editing' && row[key] !== this.backupRow[key]) {
          let record = {
            satellite_name: row.satellite_name, // Add the JCAT value here
            column: key,
            oldValue: this.backupRow[key],
            newValue: row[key],
            time: new Date().toISOString() // ISO format time of the edit
          };
          edit_records.push(record);
        }
      }

      if (edit_records.length > 0) {
        // Send the edit records to the backend
        axios.post('http://localhost:8000/api/edit-data', {
          edit_records: edit_records,
          name: this.username
        })
          .then(response => {
            console.log('Edit records sent successfully', response);
          })
          .catch(error => {
            console.error('Error sending edit records', error);
          });
      }

      // Clear the backup since changes are saved
      this.backupRow = null;
      row.editing = false;
    },
    cancelEdit(row) {
      // Restore the original data from the backup
      Object.assign(row, this.backupRow);
      row.editing = false;
    },
    filterHandler(value, row) {
      // Assuming you want to filter based on the satellite_name property
      return row.un_registry_country === value;
    },
    toggleFilters() {
      this.filtersActive = !this.filtersActive;
      // Optionally, add logic here to apply or remove filters
    },
  },
  computed: {
    filteredData() {
      // Filter based on selectedColumns and searchQuery
      return this.tableData.filter(row => {
        // Check if the satellite name contains the search query
        const matchesSearch = row.satellite_name.toLowerCase().includes(this.searchQuery.toLowerCase());

        // Check if the row's columns are selected for display
        const columnsSelected = this.selectedColumns.length === 0 || this.selectedColumns.some(col => row.hasOwnProperty(col));

        return matchesSearch && columnsSelected;
      });
    },
  },
};
</script>

<style>
.el-table {
  margin-top: 20px;
}

.el-menu--inline {
  background-color: #000c17 !important;
}

.el-menu--inline .el-menu-item {
  background-color: #000c17 !important;
  padding-left: 49px !important;
}

.el-menu-item:hover,
.el-submenu__title:hover {
  color: #fff !important;
}

.el-submenu__title:hover i {
  color: #fff !important;
}

.el-menu-item:hover i {
  color: #fff !important;
}

.el-menu-item.is-active {
  background-color: #1890ff !important;
  border-radius: 5px !important;
  width: calc(100% - 8px);
  margin-left: 4px;
}

.el-menu-item.is-active i,
.el-menu-item.is-active .el-tooltip {
  margin-left: -4px;
}

.el-menu-item {
  height: 40px !important;
  line-height: 40px !important;
}

.el-submenu__title {
  height: 40px !important;
  line-height: 40px !important;
}

.el-submenu .el-menu-item {
  min-width: 0 !important;
}

.el-menu--inline .el-menu-item.is-active {
  padding-left: 45px !important;
}

/*.el-submenu__icon-arrow {*/
/*  margin-top: -5px;*/
/*}*/

.el-aside {
  transition: width 0.3s;
  box-shadow: 2px 0 6px rgba(0, 21, 41, 0.35);
}

.logo-title {
  margin-left: 5px;
  font-size: 20px;
  transition: all 0.3s;
  /* 0.3s */
}

.el-header {
  box-shadow: 2px 0 6px rgba(0, 21, 41, 0.35);
  display: flex;
  align-items: center;
}

/* Style for the button container */
.operation-buttons {
  display: flex;
  flex-direction: column;
  /* Stack buttons vertically */
  align-items: flex-start;
  /* Align buttons to the start of the flex container */
}

/* Style for individual buttons */
.operation-button {
  margin-bottom: 8px;
  /* Add bottom margin to each button except the last one */
}

.operation-button:last-child {
  margin-bottom: 0;
  /* Remove bottom margin from the last button */
}

.el-button+.el-button {
  margin-left: 0px;
}

.el-dropdown {
  margin-left: auto;
}

.el-dropdown-menu {
  padding: 10px;
  /* Add some padding inside the dropdown */
  max-height: 300px;
  /* Set a max height */
  overflow-y: auto;
  /* Add scrollbar if content is too long */
  width: auto;
  /* Adjust width as needed */
}

/* Style for each checkbox in the dropdown */
.el-checkbox {
  display: block;
  /* Make each checkbox take up a full line */
  margin: 5px 0;
  /* Add some margin for spacing */
}

/* Style for the checkbox label */
.el-checkbox__label {
  font-size: 14px;
  /* Adjust font size as needed */
}

.el-table .cell {
  text-overflow: clip;
}

.el-radio-group {
  margin-bottom: 20px;
}

.el-button--small{
  margin: 5px;
}
</style>
