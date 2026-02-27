import { View, Text, ScrollView, Button, SectionList } from 'react-native'
import React, { useState, useEffect, useCallback } from 'react'
import TripCard from '../components/TripCard'
import { getTrips, Trip } from '../services/Trips'
import ScreenLayout from '../components/ScreenLayout'
import { SafeAreaView } from 'react-native-safe-area-context'
import  MonthYearDropdown from '../components/MonthYearDropdown'


const History = () => {
  const [loading, setIsLoading] = useState(true);
  const [trips, setTrips] = useState<Trip[]>([]);
  const [error, setError] = useState<unknown | null>(null);
  



  const handleGetAllTrips = async () => { 
  try {
    setIsLoading(true);
    const response = await getTrips();

    if (!response) {
      alert("Failed to get trip history. Please try again.");
      return;
    }

    setTrips(response);
    setIsLoading(false);

  } catch (error) {
    console.error('failed to get trips: ', error);
    alert("Failed to get trip history. Please try again.");
    setError(error);
    return;
  }
}

const groupTripsByDate = (trips: Trip[]) => {
  const grouped = trips.reduce((acc, trip) => {
    const date = new Date(trip.started_at);
    const dateKey = date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      weekday: 'short'
    });

    if (!acc[dateKey]) {
      acc[dateKey] = [];
    }
    acc[dateKey].push(trip);
    return acc;
  }, {} as Record<string, Trip[]>);
  
  return Object.keys(grouped).map(date => ({
    title: date,
    data: grouped[date]
  }));
}

  useEffect(() => {
    handleGetAllTrips();
  }, []);

  if (loading) {
    return (
      <Text>Loading...</Text>
    )
  }

  if (error) {
    return (
      <Text>Error</Text>
    )
  }

  return (
  <SafeAreaView style={{flex: 1}}>
    <SectionList
      sections={groupTripsByDate(trips)}
      keyExtractor={(item) => item.id}
      renderItem={({ item }) => (
        <TripCard
          id={item.id}
          geometry={item.geometry ?? null}
          start_address={item.start_address ?? ''}
          end_address={item.end_address ?? ''}
          mileage_reimbursement_total={item.mileage_reimbursement_total ?? 0}
          distance_meters={item.miles ?? 0}
        />
      )}
      renderSectionHeader={({ section: { title } }) => (
        <View style={{backgroundColor: '#ffffffff', padding: 12, marginTop: 20}}>
          <Text style={{fontSize: 14}}>{title}</Text>
        </View>
      )}
      ListHeaderComponent={
        <View style={{justifyContent: 'center', alignItems: 'center', backgroundColor: 'white', marginBottom: 10, height: 200}}>
            <MonthYearDropdown />
        </View>
      }
      ListEmptyComponent={
        <Text style={{textAlign: 'center', marginTop: 20}}>No Trips Found.</Text>
      }
    />
  </SafeAreaView>
  )
}

export default History