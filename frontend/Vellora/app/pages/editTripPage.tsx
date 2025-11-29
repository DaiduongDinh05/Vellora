import { View, Text } from "react-native";
import { useRouter, useLocalSearchParams } from 'expo-router';
import { getTrip, Trip } from "../services/Trips";
import TripDetailsForm from "../components/TripDetailsForm";
import { useRateOptions } from "../hooks/useRateOptions";
import GeometryMap from "../components/GeometryMap";
import ScreenLayout from "../components/ScreenLayout";
import { useState, useEffect } from "react";
import EditableNumericDisplay from "../components/EditableNumericDisplay";
import Button from "../components/Button";

const MAPBOX_KEY = process.env.EXPO_PUBLIC_API_KEY_MAPBOX_PUBLIC_ACCESS_TOKEN;


const EditTripPage = () => {
    const router = useRouter();
    const { id } = useLocalSearchParams();

    // states
    const [trip, setTrip] = useState<Trip | null>(null);
    const [isTripLoading, setTripLoading] = useState<boolean>(false);
    const [notes, setNotes] = useState<string>('')
    const [vehicle, setVehicle] = useState<string | null>('');
    const [tripValue, setTripValue] = useState<number | null>(0.00);
    const [parking, setParking] = useState<number>(0.00);
    const [tolls, setTolls] = useState<number>(0.00)
    const [gas, setGas] = useState<number>(0.00)
    const [tripDistance, setTripDistance] = useState<number>(0)
    const [startAddress, setStartAddress] = useState<string>('');
    const [endAddress, setEndAddress] = useState<string>('');
    const [tripGeometry, setTripGeometry] = useState<object | null>(null);
    const [error, setError] = useState<string | null>(null);

     const { rateItems, categoryItems, loading } = useRateOptions();

    const handleGetTrip = async () => {
        const tripId = id as string | undefined;
        if (!tripId) return;

        setTripLoading(true);
        const response = await getTrip(tripId);
        
        if (!response) {
            alert("Trip not found, please try again.");
            setTripLoading(false);
            return;
        }

        setTrip(response);
        setTripLoading(false);
    }

    const handleUpdateTrip = async () => {
        // logic here
    }
    
    
    // get the trip with passed id
    useEffect(() => {
        if (id) {
            handleGetTrip();
        }
    }, [id]);
    
    // use effect for syncing the current state of trip once loaded
    useEffect(() => {
        if(!trip) return;
        setNotes(trip.purpose ?? '');
        setVehicle(trip.vehicle ?? null);
        setTripValue(trip.mileage_reimbursement_total ?? 0.00);
        const expenses = trip.expenses ?? []
        setParking(expenses.find(e => e.type === 'Parking' || 'parking')?.amount ?? 0.00);
        setTolls(expenses.find(e => e.type === 'tolls' || 'Tolls')?.amount?? 0.00);
        setGas(expenses.find(e => e.type === 'gas' || 'Gas')?.amount ?? 0.00);
        setTripDistance(trip.miles ?? 0);
        setStartAddress(trip.start_address ?? '');
        setEndAddress(trip.end_address ?? '');
        setTripGeometry(trip.geometry ?? null);
    }, [trip])

    if (isTripLoading) {
        return (
            <Text>Loading...</Text>
        )
    }

    if (error) {
        return (
            <Text>Error: ${error}</Text>
        )
    }

    return (
        
        <ScreenLayout
            footer={
                <>
                    <View className='flex-row jusitfy-between mb-4'>
                        <EditableNumericDisplay
                            label='Value'
                            value={tripValue != null ? String(tripValue) : '0.00'}
                            onChangeText={(text) => {
                                const trimmed = text.trim();
                                const parsed = trimmed === '' ? null : Number(trimmed);
                                setTripValue(parsed as number | null);
                            }}
                            unit='$'
                        />
                        <EditableNumericDisplay
                            label='Distance'
                            value={tripDistance != null ? String(tripDistance) : '0.00'}
                            onChangeText={(text) => {
                                const trimmed = text.trim();
                                const parsed = trimmed === '' ? null : Number(trimmed);
                                setTripValue(parsed as number | null);
                            }}
                            unit='mi'
                        />
                    </View>
                    <Button
                        title="Update Trip"
                        onPress={handleUpdateTrip}
                        style={{top: 10}}
                    />
                </>
            }
        >
            <View style={{height: 300, width: '100%', overflow: 'hidden'}}>
                <GeometryMap geometry={tripGeometry}/>
            </View>
            
        </ScreenLayout>
    );
}

export default EditTripPage;