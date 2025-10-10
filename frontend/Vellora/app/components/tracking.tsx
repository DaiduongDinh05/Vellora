import {  View, Text  } from "react-native";
import { useState, useEffect } from "react";
import * as Location from 'expo-location';

function Tracking() { 
    const [location, setLocation] = useState<Location.LocationObject | null>(null);
    const [errorMsg, setErrorMsg] = useState<string | null>(null);

    useEffect(() => {
        async function getCurrentLocation() {
            let { status } = await Location.requestForegroundPermissionsAsync(); // Request Location Permissions from Phone
            if (status !== 'granted') { // Check if Granted
                setErrorMsg('Permission to access location was denied. Please enable location.');
                return;
            }

            let location = await Location.getCurrentPositionAsync({});
            setLocation(location);
        }

        getCurrentLocation();
    }, []);

    let text = 'Waiting...';
    if (errorMsg) {
        text = errorMsg;
    } else if (location) {
        text = JSON.stringify(location);
    }

    return (
    <Text>This is the Tracking Component, Location: {text}</Text>
    )
}



export default Tracking;