import React from 'react'
import {  View, Text, Button  } from "react-native";
import { useState, useEffect } from "react";
import * as Location from 'expo-location';
import * as TaskManager from 'expo-task-manager';
import { get } from 'react-native/Libraries/TurboModule/TurboModuleRegistry';

const LOCATION_TASK_NAME = 'background_location_tracking';

TaskManager.defineTask(LOCATION_TASK_NAME, async ({ data, error }) => {
        if (error) {
            console.log(error.message)
            return;
        }
                
               const { locations } = data;
                console.log(locations[0]) // TODO: FIX COORDS IN OBJ
            });


function LocationTracker()  { 
    const [errorMessage, setErrorMessage] = useState<string | null>(null);
    const [isTracking, setIsTracking] = useState(false);

    async function getPermissions() {
        try {
                const { status: foregroundPermissions } = await Location.requestForegroundPermissionsAsync(); // have to request Foreground before BG
                        if (!foregroundPermissions) { // Check if Granted
                                setErrorMessage('Permission to access location was denied. Please enable location.');
                                return false;
                        }

                        let { status: backgroundPermssions } = await Location.requestBackgroundPermissionsAsync(); // Request Background Location for Tracking
                        if (backgroundPermssions !== "granted" ) {
                                setErrorMessage('Permission to access background location was denied, Please enable background location for best performance.')
                                return false;
                        }
        return true;

        } catch (error) {
                console.error('Error getting permissions: ', error)
                return false;
        }
    }

    async function startTracking() {
        try {
            // Get Perms for Location Tracking
            const hasPermissions = await getPermissions();
            if (!hasPermissions) return;

            await Location.startLocationUpdatesAsync(LOCATION_TASK_NAME, {
                accuracy: Location.Accuracy.Balanced,
                deferredUpdatesInterval: 30000,
                deferredUpdatesDistance: 8100,
                // For android to allow background location services
                foregroundService: {
                    notificationTitle: 'Location Tracking is Active',
                    notificationBody: 'Your Location is being tracked in the background.',
                },
            });
            
        } catch (error) {
            console.error('Error to start tracking: ', error);
            return;
        }
            
    };




    useEffect(() => {
       startTracking();
    }, []);



    return (
        <View>
            <Text>tracking</Text>
        </View>
      
    )
}



export default LocationTracker;