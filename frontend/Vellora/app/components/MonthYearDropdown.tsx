import React, { useState } from "react";
import { View, Text } from 'react-native';
import MonthPicker from 'react-native-month-year-picker';





const MonthYearDropdown = () => {
    const [date, showDate] = useState<Date>(new Date());
    const [show, setShow] = useState<boolean>(false);
}





export default MonthYearDropdown;