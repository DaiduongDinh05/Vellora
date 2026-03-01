import React, { useState, useCallback } from "react";
import { View, Text, TouchableOpacity, Button } from 'react-native';
import MonthPicker from 'react-native-month-year-picker';

interface MonthYearDropdownProps {
  currentDate: Date
}



const MonthYearDropdown: React.FC<MonthYearDropdownProps> = ({ currentDate }) => {
    const [date, setDate] = useState<Date>(currentDate);
    const [show, setShow] = useState<boolean>(false);
    
    const showPicker = useCallback((value: boolean | ((prevState: boolean) => boolean)) => setShow(value), []);

    const onValueChange = useCallback((event: any, newDate: Date) => {
      const selectedDate = newDate || date;
      setDate(selectedDate);
      setShow(false);
    },
    [date, showPicker],
  );

  return (
    <View style={{justifyContent: 'center', alignItems: 'center'}}>
        <TouchableOpacity onPress={() => showPicker(true)}>
            <Text className='text-2xl font-bold text-primaryPurple text-center mt-2 mb-8'>{date.toLocaleDateString('en-us', { month: 'long', year: 'numeric'})}</Text>
        </TouchableOpacity>
        { show && (
          <View style={{ width: "100%", alignItems: "center", height: 300, paddingBottom: 52 }}>
            <MonthPicker
            onChange={onValueChange}
            value={date}
            minimumDate={new Date(2020, 0)}
            maximumDate={new Date(2050, 11)} />
          </View>
        )}
    </View>
  )


}

export default MonthYearDropdown;