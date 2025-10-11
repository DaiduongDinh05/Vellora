import {  View, Text  } from "react-native";
import { useState, useEffect } from "react";
import * as Location from 'expo-location';
import * as TaskManager from 'expo-task-manager';

const LOCATION_TASK = 'background-location-tracking';


function startBackgroundTracking() { 
    const [location, setLocation] = useState<Location.LocationObject | null>(null);
    const [errorMsg, setErrorMsg] = useState<string | null>(null);
    const [subscription, setSubscription] = useState<Location.LocationSubscription | null>(null);

    async function startTracking() {
        // Get Perms for Location Tracking
            const foregroundPermissions = await Location.requestForegroundPermissionsAsync(); // Request Location Permissions from Phone, have to request Foreground before BG
            if (!foregroundPermissions) { // Check if Granted
                setErrorMsg('Permission to access location was denied. Please enable location.');
                return;
            }

            let { status: backgroundPermssions } = await Location.requestBackgroundPermissionsAsync(); // Request Background Location for Tracking
            if (backgroundPermssions !== "granted" ) {
                setErrorMsg('Permission to access background location was denied, Please enable background location for best performance.')
                return;
            }

            const locationSubscription = await Location.watchPositionAsync({            // Subscription for Position Watching
            accuracy: Location.LocationAccuracy.BestForNavigation,                      // Most accurate for Nav
            timeInterval: 5000,                                                         // 5000 ms,
            distanceInterval: 10                                                        // 10 meters
        }, 
            (newLocation) => {
                setLocation(newLocation);                                               // Update Location
                console.log(newLocation)
            },
        );
        setSubscription(locationSubscription);
    };



    useEffect(() => {
        startTracking();
    }, []);



    return (
    <Text>This is the Tracking Component</Text>
    )
}



export default startBackgroundTracking;