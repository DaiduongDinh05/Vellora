import React from 'react'
import {  View, Text, Button  } from "react-native";
import { useState, useEffect } from "react";
import * as Location from 'expo-location';
import * as TaskManager from 'expo-task-manager';

const LOCATION_TASK_NAME = 'background_location_tracking';


function startBackgroundTracking() { 
    const [location, setLocation] = useState<Location.LocationObject | null>(null);
    const [errorMsg, setErrorMsg] = useState<string | null>(null);
    const [subscription, setSubscription] = useState<Location.LocationSubscription | null>(null);

    async function startTracking() {
        // Get Perms for Location Tracking
            const foregroundPermissions = await Location.requestForegroundPermissionsAsync(); // have to request Foreground before BG
            if (!foregroundPermissions) { // Check if Granted
                setErrorMsg('Permission to access location was denied. Please enable location.');
                return;
            }

            let { status: backgroundPermssions } = await Location.requestBackgroundPermissionsAsync(); // Request Background Location for Tracking
            if (backgroundPermssions !== "granted" ) {
                setErrorMsg('Permission to access background location was denied, Please enable background location for best performance.')
                return;
            }
            
            if (backgroundPermssions === "granted") {
                await Location.startLocationUpdatesAsync(LOCATION_TASK_NAME, {
                accuracy: Location.Accuracy.Balanced,
                });
            }
    };

    TaskManager.defineTask(LOCATION_TASK_NAME, async ({ data, error }) => {
                if (error) {
                    console.log(error.message)
                    return;
                }
                
                // let { locations } = data;
                console.log(data) // TODO: FIX COORDS IN OBJ
            })



    useEffect(() => {
       startTracking();
    }, []);



    return (
        <View>
            <Text>tracking</Text>
        </View>
      
    )
}



export default startBackgroundTracking;