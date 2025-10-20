import { View, Text, ImageBase, useColorScheme } from 'react-native'
import React from 'react'
import { Tabs } from 'expo-router'
import { Colors } from '../Colors';
import { FontAwesome } from '@expo/vector-icons';

const _layout = () => {
  return (
    <Tabs
      screenOptions={{
        tabBarShowLabel: false, // Hide the labels

        // For the tabs background color
        tabBarStyle: {
          backgroundColor: '#404CCF',
          height: 80,
          borderTopWidth: 0, // remove top line
        },
      }}
    
    
    >
        <Tabs.Screen
            name='index'
            options={{
                title: 'Home', // home tab
                headerShown: false,
                tabBarIcon: ({ focused }) => ( // load icon
                  <TabIcon 
                    icon="home"
                    color={focused ? Colors.primaryPurple : Colors.textWhite} // change color when clicked
                    focused={focused}
                  />
                )
            }}
        />

        <Tabs.Screen
            name='history'
            options={{
                title: 'History', // history tab
                headerShown: false,
                tabBarIcon: ({ focused }) => ( // load icon
                  <TabIcon 
                    icon="history"
                    color={focused ? Colors.primaryPurple : Colors.textWhite} // change color when clicked
                    focused={focused}
                  />
                )
            }}
        />

        <Tabs.Screen   
            name='stats'
            options={{
                title: 'Statistics', // stats tab
                headerShown: false,
                tabBarIcon: ({ focused }) => ( // load icon
                  <TabIcon 
                    icon="bar-chart"
                    color={focused ? Colors.primaryPurple : Colors.textWhite} // change color when clicked
                    focused={focused}
                  />
                )
            }}
        />

        <Tabs.Screen 
            name='profile' 
            options={{
                title: 'Profile', // profile tab
                headerShown: false,
                tabBarIcon: ({ focused }) => ( // load icon
                  <TabIcon 
                    icon="user"
                    color={focused ? Colors.primaryPurple : Colors.textWhite} // change color when clicked
                    focused={focused}
                  />
                )
            }}
        />
        
    </Tabs>
  )
};

// Helper reusable component for the tab icons
const TabIcon = ({ icon, color, focused }: { icon: any; color: string; focused: boolean }) => {
  return (

    // Return contained for the icon
    <View
      style={{
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: focused ? Colors.textWhite : 'transparent',
        marginTop: 30,
        height: 60,
        width: 60,
        borderRadius: 12,
      }}
    >
      <FontAwesome name={icon} size={28} color={color}/>


    </View>
  )
}

export default _layout