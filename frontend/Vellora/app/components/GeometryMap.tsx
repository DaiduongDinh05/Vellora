import { StyleSheet, View } from 'react-native';
import React from 'react';
import geometry from '../constants/testGeo.json'
import MapboxGL from '@rnmapbox/maps';

// get mapbox access token
const MAPBOX_KEY = process.env.EXPO_PUBLIC_API_KEY_MAPBOX_PUBLIC_ACCESS_TOKEN;
MapboxGL.setAccessToken(`${MAPBOX_KEY}`);

const GeometryMap = () => {
    return (
        <View style={styles.container}>

            {/* main map component */}
            <MapboxGL.MapView style={styles.map}>

                {/* configure the map's view point */}
                <MapboxGL.Camera 
                    zoomLevel={12}                              // zoom in
                    centerCoordinate={[-122.061293, 37.332867]}        // center the coordinate
                    animationMode={'none'}                      // disable animations
                />

                {/* load the geoJSON data source for the map. "as any" bypasses typescript checks */}
                <MapboxGL.ShapeSource id="line-source" shape={geometry as any}>

                    {/* linelayer to visualize the geoJSON */}
                    <MapboxGL.LineLayer 
                        id="linelayer"
                        style={{
                            // style the route line
                            lineCap: 'round',
                            lineJoin: 'round',
                            lineOpacity: 1,
                            lineWidth: 8.0,
                            lineColor: '#404CCF',
                        }}
                    />
                </MapboxGL.ShapeSource>



            </MapboxGL.MapView>
        </View>
    )
}

export default GeometryMap

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',       // center veritcally
        alignItems: 'center',           // center horizontally
    },
    map: {
        flex: 1,
        alignSelf: 'stretch',           // stretch full container width
    },
})