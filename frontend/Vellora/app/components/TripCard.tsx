import { View, Text, Pressable } from "react-native";
import React from 'react';
import GeometryMap from "./GeometryMap";

// start address
// end address

// value - amount of miles

const sampleGeometry: object = {"coordinates": [[-122.061293, 37.332867], [-122.064478, 37.333984], [-122.066543, 37.334406], [-122.068987, 37.334437], [-122.071987, 37.333929], [-122.07274, 37.333793], [-122.075191, 37.333578], [-122.077674, 37.333954], [-122.07982, 37.334892], [-122.082163, 37.336633], [-122.083291, 37.337433]], "type": "LineString"}


const TripCard = () => {

    return (
        <View style={{justifyContent: 'flex-start', alignItems: 'center', width: '100%', height: '20%', flexDirection:'row', borderTopWidth: 2, borderBottomWidth: 2, borderColor: 'gray'}}>
            <View style={{ height: 125, width: 125, overflow: 'hidden', borderRadius: 10, marginLeft: 30 }}>
                <GeometryMap geometry={sampleGeometry}/>
            </View>
            <View>
                <View style={{marginBottom: 40, marginLeft: 10, marginTop: 20}}> 
                    <Text>{'\u2022'} Start</Text>
                    <Text>{'\u2022'} End</Text>
                </View>
                <View style={{marginBottom: 40, marginLeft: 50}}>
                    <Text style={{color: '#4DBF69'}}>$Value - Distance mi</Text>
                </View>
            </View>
        </View>
    )
}


export default TripCard