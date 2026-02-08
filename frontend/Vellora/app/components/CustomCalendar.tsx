import React, { useState } from 'react';
import { View, Text, FlatList, StyleSheet } from 'react-native';
import { Calendar, DateData } from 'react-native-calendars';

// define the shape of a single trip item
interface AgendaItem {
  id: string;
  time: string;
  purpose: string;
  address: string;
  type: string;
}

// define the shape of your schedule data object
const MOCK_SCHEDULES: Record<string, AgendaItem[]> = {
  '2026-02-08': [
    { id: '1', time: '09:00 AM', purpose: 'Meeting with Client X', address: '123 Tech Blvd', type: 'Business' },
    { id: '2', time: '02:00 PM', purpose: 'Site Visit', address: '456 Construction Rd', type: 'Business' }
  ],
  '2026-02-10': [
    { id: '3', time: '11:30 AM', purpose: 'Lunch with Mentor', address: '789 Downtown Ave', type: 'Personal' }
  ]
};

const CustomCalendar = () => {
  const [selected, setSelected] = useState('');
  const today = new Date().toISOString().split('T')[0]; // get today's date in YYYY-MM-DD format

  const getMarkedDates = () => {
    const marks: any = {};
    const CIRCLE_SIZE = 40;

    // add dots for days with scheduled trips
    Object.keys(MOCK_SCHEDULES).forEach(date => {
      marks[date] = { marked: true, dotColor: '#404CCF' };
    });

    // style "today"
    marks[today] = {
      ...(marks[today] || {}),
      customStyles: {
        container: {
          backgroundColor: '#404CCF',
          borderRadius: CIRCLE_SIZE / 2,
          justifyContent: 'center',
          alignItems: 'center',
          width: CIRCLE_SIZE,
          height: CIRCLE_SIZE,
        },
        text: {
          color: 'white',
          fontWeight: 'bold'
        }
      }   
    };

    // style the selected day
    if (selected) {
      marks[selected] = {
        ...(marks[selected] || {}),
        customStyles: {
          container: {
            backgroundColor: 'white',
            borderColor: '#404CCF',
            borderWidth: 2,
            borderRadius: CIRCLE_SIZE / 2,
            justifyContent: 'center',
            alignItems: 'center',
            width: CIRCLE_SIZE,
            height: CIRCLE_SIZE,
          },
          text: {
            color: '#404CCF',
            fontWeight: 'bold'
          }
        }
      };
    }

    return marks;
  };

  const renderAgendaItem = (item: AgendaItem ) => (
    <View key={item.id} style={styles.card}>
      <View style={styles.cardTimeContainer}>
        <Text style={styles.cardTime}>{item.time}</Text>
        <View style={styles.verticalLine} />
      </View>
      <View style={styles.cardContent}>
        <Text style={styles.cardPurpose}>{item.purpose}</Text>
        <Text style={styles.cardAddress}>{item.address}</Text>
        <View style={styles.badgeContainer}>
          <Text style={styles.badgeText}>{item.type}</Text>
        </View>
      </View>
    </View>
  );

  const dailyTrips = MOCK_SCHEDULES[selected] || [];

  return (
    <View style={styles.container}>
      
      <Calendar
        markingType={'custom'}      // enable custom styling
        onDayPress={(day: DateData) => {
          setSelected(day.dateString);
        }}

        // dynamic marks
        markedDates={getMarkedDates()}

        theme={{
          todayTextColor: '#404CCF',
          arrowColor: '#404CCF',
        }}
      />

      <View style={styles.agendaContainer}>
        <Text style={styles.headerTitle}>
          {selected ? `Schedule for ${selected}` : 'Select a date to view trips'}
        </Text>

        <View>
          {dailyTrips.length > 0 ? (
            dailyTrips.map(item => renderAgendaItem(item))
          ) : (
            selected ? (
              <Text style={styles.emptyText}>No trips scheduled for this day.</Text>
            ) : null
          )}
        </View> 
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
  },
  agendaContainer: {
    flex: 1,
    padding: 16,
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 12,
  },
  emptyText: {
    color: '#999',
    fontStyle: 'italic',
    marginTop: 10,
  },
  card: {
    flexDirection: 'row',
    backgroundColor: 'white',
    borderRadius: 12,
    marginBottom: 12,
    padding: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 2,
  },
  cardTimeContainer: {
    alignItems: 'center',
    marginRight: 16,
    width: 60,
  },
  cardTime: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 4,
  },
  verticalLine: {
    flex: 1,
    width: 2,
    backgroundColor: '#F0F0F0',
    marginTop: 4,
  },
  cardContent: {
    flex: 1,
    justifyContent: 'center',
  },
  cardPurpose: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 4,
  },
  cardAddress: {
    fontSize: 14,
    color: '#666',
    marginBottom: 8,
  },
  badgeContainer: {
    backgroundColor: '#EEEFFF',
    alignSelf: 'flex-start',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 6,
  },
  badgeText: {
    color: '#404CCF',
    fontSize: 12,
    fontWeight: '600',
  }
});

export default CustomCalendar;