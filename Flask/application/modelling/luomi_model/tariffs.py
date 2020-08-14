import numpy as np
import pandas as pd
import datetime
import io


class Tariffs():

    def __init__(self, tariff_config_dict):
        self.config = tariff_config_dict
        print("What you're looking for", self.config['retail']['daily_charge'])
    
    # --------------------------------------------------------------
    # Retail component
    # --------------------------------------------------------------
    def get_retail_variable_tariff(self, date_time, retail_tariff_type):
        # Get data from df
        
        offpeak_charge = float(self.config['retail']['off_peak_tariff'])
        shoulder_charge	= float(self.config['retail']['shoulder_tariff'])
        peak_charge	= float(self.config['retail']['peak_tariff'])
        
        block_1_charge = float(self.config['retail']['block_1_tariff'])
        block_2_charge = float(self.config['retail']['block_2_tariff'])
        block_1_volume = float(self.config['retail']['block_1_volume'])
        block_2_volume = float(self.config['retail']['block_2_volume'])
        
        shoulder_start_time = float(self.config['tou_times'][0])
        shoulder_end_time = float(self.config['tou_times'][1])
        peak_start_time = float(self.config['tou_times'][1])
        peak_end_time = float(self.config['tou_times'][2])
        peak_start_time_2 = float(self.config['tou_times'][1])  # Making these the same - just going to have one peak for the moment but leaving the option for 2.
        peak_end_time_2 = float(self.config['tou_times'][2])
        shoulder_start_time_2 = float(self.config['tou_times'][2])
        shoulder_end_time_2 = float(self.config['tou_times'][3])

        demand_charge = float(self.config['retail']['demand_charge'])
        tou_weekday_only_flag = float(self.config['retail']['tou_weekday_only'])

        if retail_tariff_type == 'Block':
            variable_tariff = (block_1_charge, block_2_charge, block_1_volume)
        elif retail_tariff_type == 'TOU':
            variable_tariff = (peak_charge, shoulder_charge, offpeak_charge, peak_start_time, peak_end_time, peak_start_time_2, peak_end_time_2, shoulder_start_time, shoulder_end_time, shoulder_start_time_2, shoulder_end_time_2, tou_weekday_only_flag, demand_charge)
        else:
            raise ValueError('Retail tariff type not known:'+str(retail_tariff_type))

        return variable_tariff

    def get_retail_fixed_tariff(self, fixed_period_minutes, retail_tariff_type):
        """Fixed tariff component from retail tariff data. Returns fixed value expressed per fixed period minutes (input)."""
        # print(self.config['retail']['daily_charge'], type(self.config['retail']['daily_charge']))
        fixed_tariff = float(self.config['retail']['daily_charge']) * (float(fixed_period_minutes)/float(60*24))
        return fixed_tariff

    def get_retail_spot_tariff(self, fixed_period_minutes, retail_tariff_type):
        # """Spot tariff component from retail tariff data. Returns fixed value expressed per fixed period minutes (input)."""
        # spot_tariff = float(self.config['retail']['spot_tariff']) * (float(fixed_period_minutes)/float(60*24))
        """Spot tariff component from retail tariff data."""
        spot_tariff = float(self.config['retail']['spot_tariff'])
        return spot_tariff

    def get_retail_solar_feed_in_tariff(self,date_time, retail_tariff_type, solar_capacity):
        """Solar FiT component from retail tariff data."""
        return float(self.config['retail']['feed_in_tariff'])

    # --------------------------------------------------------------
    # Network component
    # --------------------------------------------------------------
    # TUOS - Transmission use of service charges - will presumably be zero for local solar and battery import
    def get_tuos_on_grid_import_fixed(self, fixed_period_minutes, tuos_tariff_type):
        fixed_tariff = float(self.config['tuos']['daily_charge']) * (float(fixed_period_minutes)/float(60*24))
        return fixed_tariff

    def get_tuos_on_grid_import_variable(self, date_time, tuos_tariff_type):    
        """Variable tariff component from TUOS tariff data."""
        # Get data from df
       
        offpeak_charge = float(self.config['tuos']['off_peak_tariff'])
        shoulder_charge	= float(self.config['tuos']['shoulder_tariff'])
        peak_charge	= float(self.config['tuos']['peak_tariff'])
        shoulder_start_time	= float(self.config['tou_times'][0])
        shoulder_end_time = float(self.config['tou_times'][1])
        peak_start_time	= float(self.config['tou_times'][1])
        peak_end_time = float(self.config['tou_times'][2])
        peak_start_time_2 = float(self.config['tou_times'][1]) #Making these the same - just going to have one peak for the moment but leaving the option for 2. 
        peak_end_time_2	= float(self.config['tou_times'][2])
        shoulder_start_time_2 = float(self.config['tou_times'][2])
        shoulder_end_time_2	= float(self.config['tou_times'][3])
        demand_charge = float(self.config['tuos']['daily_charge'])
        tou_weekday_only_flag = float(self.config['tuos']['tou_weekday_only'])

        # Note, demand charge included in returned values to make calculations in main.py nicer to work with (avoid repeating TOU calcs for demand charge case)
        variable_tariff = (peak_charge, shoulder_charge, offpeak_charge, peak_start_time, peak_end_time, peak_start_time_2, peak_end_time_2, shoulder_start_time, shoulder_end_time, shoulder_start_time_2, shoulder_end_time_2, tou_weekday_only_flag, demand_charge)
        return variable_tariff

    # Things the network is paid (fixed DUOS charges, variable DUOS charges, local solar DUOS charges, central battery DUOS charges)
    # Apply to amounts consumer each time period then sum for total network income
    def get_duos_on_grid_import_fixed(self, fixed_period_minutes, duos_tariff_type):
        fixed_tariff = float(self.config['duos']['daily_charge']) * (float(fixed_period_minutes)/float(60*24))
        return fixed_tariff

    def get_duos_on_grid_import_variable(self, date_time, duos_tariff_type):
        """Variable tariff component from DUOS tariff data."""
        # Get data from df
        
        offpeak_charge = float(self.config['duos']['off_peak_tariff'])
        shoulder_charge	= float(self.config['duos']['shoulder_tariff'])
        peak_charge	= float(self.config['duos']['peak_tariff'])
        shoulder_start_time	= float(self.config['tou_times'][0])
        shoulder_end_time = float(self.config['tou_times'][1])
        peak_start_time	= float(self.config['tou_times'][1])
        peak_end_time = float(self.config['tou_times'][2])
        peak_start_time_2 = float(self.config['tou_times'][1]) #Making these the same - just going to have one peak for the moment but leaving the option for 2. 
        peak_end_time_2	= float(self.config['tou_times'][2])
        shoulder_start_time_2 = float(self.config['tou_times'][2])
        shoulder_end_time_2	= float(self.config['tou_times'][3])
        demand_charge = float(self.config['duos']['demand_charge'])
        tou_weekday_only_flag = float(self.config['duos']['tou_weekday_only'])

        # Note, demand charge included in returned values to make calculations in main.py nicer to work with (avoid repeating TOU calcs for demand charge case)
        variable_tariff = (peak_charge, shoulder_charge, offpeak_charge, peak_start_time, peak_end_time, peak_start_time_2, peak_end_time_2, shoulder_start_time, shoulder_end_time, shoulder_start_time_2, shoulder_end_time_2, tou_weekday_only_flag, demand_charge)
        return variable_tariff
    
    # Network use of service charges (TUOS + DUOS + green schemes and friends) - will presumably be zero for local solar and battery import
    def get_nuos_on_grid_import_fixed(self, fixed_period_minutes, nuos_tariff_type):
        # print("!!!!!!!!!!!!!!!!!!!!!!!")
        # print(self.nuos_tariff_data)
        # print("!!!!!!!!!!!!!!!!!!!!!!!")
        fixed_tariff = float(self.config['nuos']['daily_charge']) * (float(fixed_period_minutes)/float(60*24))
        return fixed_tariff

    def get_nuos_on_grid_import_variable(self, date_time, nuos_tariff_type):
        """Variable tariff component from NUOS tariff data."""
        # Get data from df
        
        offpeak_charge = float(self.config['nuos']['off_peak_tariff'])
        shoulder_charge	= float(self.config['nuos']['shoulder_tariff'])
        peak_charge	= float(self.config['nuos']['peak_tariff'])
        shoulder_start_time	= float(self.config['tou_times'][0])
        shoulder_end_time = float(self.config['tou_times'][1])
        peak_start_time	= float(self.config['tou_times'][1])
        peak_end_time = float(self.config['tou_times'][2])
        peak_start_time_2 = float(self.config['tou_times'][1]) #Making these the same - just going to have one peak for the moment but leaving the option for 2. 
        peak_end_time_2	= float(self.config['tou_times'][2])
        shoulder_start_time_2 = float(self.config['tou_times'][2])
        shoulder_end_time_2	= float(self.config['tou_times'][3])
        demand_charge = float(self.config['nuos']['demand_charge'])
        tou_weekday_only_flag = float(self.config['nuos']['tou_weekday_only'])

        # Note, demand charge included in returned values to make calculations in main.py nicer to work with (avoid repeating TOU calcs for demand charge case)
        variable_tariff = (peak_charge, shoulder_charge, offpeak_charge, peak_start_time, peak_end_time, peak_start_time_2, peak_end_time_2, shoulder_start_time, shoulder_end_time, shoulder_start_time_2, shoulder_end_time_2, tou_weekday_only_flag, demand_charge)
        return variable_tariff 

    # --------------------------------------------------------------
    # Local solar component
    # --------------------------------------------------------------
    def get_energy_income_on_local_solar_import_from_peer(self, date_time):
        """Amount participant is paid by retailer to sell solar to neighbour."""
        return float(self.config['local_solar']['energy'])

    def get_total_local_solar_import_from_peer_tariff(self, date_time):
        """Amount participant pays retailer to buy solar from neighbour."""
        local_solar_import_tariff = self.get_energy_income_on_local_solar_import_from_peer(date_time) + self.get_retail_income_on_local_solar_import_from_peer(date_time) + self.get_duos_on_local_solar_import_from_peer(date_time) + self.get_tuos_on_local_solar_import_from_peer(date_time)
        return local_solar_import_tariff
    
    def get_retail_income_on_local_solar_import_from_peer(self, date_time):
        """Amount participant pays as retail margin to retailer to buy solar from neighbour."""
        return float(self.config['local_solar']['retail'])

    def get_duos_on_local_solar_import_from_peer(self, date_time):
        """Amount participant pays as DUOS to retailer to buy solar from neighbour."""
        return float(self.config['local_solar']['duos'])
    
    def get_tuos_on_local_solar_import_from_peer(self, date_time):
        """Amount participant pays as TUOS to retailer to buy solar from neighbour."""
        return float(self.config['local_solar']['tuos'])

    def get_nuos_on_local_solar_import_from_peer(self, date_time):
        """Amount participant pays as NUOS to retailer to buy solar from neighbour."""
        return float(self.config['local_solar']['duos']) + float(self.config['local_solar']['tuos'])

    # --------------------------------------------------------------
    # Central battery component
    # --------------------------------------------------------------
    def get_central_battery_owner(self):
        """Specifies battery owner as either DNSP or Third Party."""
        return self.config['central_battery']['owner']


    # Participant to battery

    def get_energy_income_on_central_batt_solar_import(self, date_time):
        """Amount participant is paid by retailer to sell solar to battery owner."""
        return float(self.config['central_battery']['local_solar_import_energy'])

    def get_total_central_batt_solar_import_tariff(self, date_time):
        """Amount battery owner pays retailer to buy solar from participant."""
        total_battery_import_tariff = self.get_energy_income_on_central_batt_solar_import(date_time) + self.get_retail_income_on_central_batt_solar_import(date_time) + self.get_duos_on_central_batt_solar_import(date_time) + self.get_tuos_on_central_batt_solar_import(date_time)
        return total_battery_import_tariff

    def get_retail_income_on_central_batt_solar_import(self, date_time):
        """Amount battery owner pays as retail margin to retailer to buy solar from participant."""
        return float(self.config['central_battery']['local_solar_import_retail'])

    def get_duos_on_central_batt_solar_import(self, date_time):
        """Amount battery owner pays as DUOS to retailer to buy solar from participant."""
        return float(self.config['central_battery']['local_solar_import_duos'])

    def get_tuos_on_central_batt_solar_import(self, date_time):
        """Amount battery owner pays as TUOS to retailer to buy solar from participant."""
        return float(self.config['central_battery']['local_solar_import_tuos'])

    def get_nuos_on_central_batt_solar_import(self, date_time):
        """Amount battery owner pays as NUOS to retailer to buy solar from participant."""
        return float(self.config['central_battery']['local_solar_import_nuos'])


    # Battery to participant
    
    def get_energy_income_on_central_batt_export(self, date_time):
        """Amount battery owner is paid by retailer to sell to participant."""
        return float(self.config['central_battery']['battery_energy'])

    def get_total_central_batt_export_tariff(self, date_time):
        """Amount participant pays retailer to buy from battery."""
        total_battery_import_tariff = self.get_energy_income_on_central_batt_export(date_time) + self.get_retail_income_on_central_batt_export(date_time) + self.get_duos_on_central_batt_export(date_time) + self.get_tuos_on_central_batt_export(date_time)
        return total_battery_import_tariff

    def get_retail_income_on_central_batt_export(self, date_time):
        """Amount participant pays as retail margin to retailer to buy from battery."""
        return float(self.config['central_battery']['retail'])

    def get_duos_on_central_batt_export(self, date_time):
        """Amount participant pays as DUOS to retailer to buy from battery."""
        return float(self.config['central_battery']['duos'])

    def get_tuos_on_central_batt_export(self, date_time):
        """Amount participant pays as TUOS to retailer to buy from battery."""
        return float(self.config['central_battery']['tuos'])

    def get_nuos_on_central_batt_export(self, date_time):
        """Amount participant pays as NUOS to retailer to buy from battery."""
        return float(self.config['central_battery']['nuos'])

# test_tariff = Tariffs('test_scheme',"data/retail_tariffs.csv","data/duos.csv","test", "data/ui_tariffs_eg.csv")
# test_tariff.get_total_central_batt_solar_import_tariff('a')
# test_tariff.get_energy_income_on_central_batt_export('a')
# print(test_tariff.get_retail_variable_tariff(30,'Business TOU'))
