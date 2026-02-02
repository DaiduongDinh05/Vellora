import { Text, View } from 'react-native'
import React from 'react'
import {Calendar, CalendarList, Agenda, LocaleConfig} from 'react-native-calendars';
import { useState } from 'react';

const CustomCalendar = () => {
    const [selected, setSelected] = useState('');

    return (
        <Calendar
        onDayPress={day => {
            setSelected(day.dateString);
        }}
        markedDates={{
            [selected]: {selected: true, disableTouchEvent: true, selectedColor: 'orange'}
        }}
        />
    );
}

export default CustomCalendar
