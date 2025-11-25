import { TextInput, FlatList, StyleSheet, TouchableOpacity, ActivityIndicator, Text, View } from 'react-native'
import React, {useState, useEffect } from 'react'
import { FontAwesome } from '@expo/vector-icons'

const MAPBOX_KEY = process.env.EXPO_PUBLIC_API_KEY_MAPBOX_PUBLIC_ACCESS_TOKEN;

// type safety
type AddressInputProps = {
    label?: string;
    placeholder?: string;
    value: string;
    onChangeText: (text: string) => void;
    onAddressSelect: (addressData: any) => void;    // callback with address details
    mapboxAccessToken: string;
    icon?: React.ReactNode;
    className?: string;
}

const AddressInput: React.FC<AddressInputProps> = ({
    label,
    placeholder = "Enter address",
    value,
    onChangeText,
    onAddressSelect,
    mapboxAccessToken,
    icon,
    className = '',
}) => {

    const [suggestions, setSuggestions] = useState<any[]>([]);  // suggested addresses based on users input
    const [isLoading, setIsLoading] = useState(false);

    // wait for 500 ms after typing stops before calling the API for locations
    useEffect(() => {

        // handle the case when the user did not type in anything yet
        if (!value || value.length < 3) {
            setSuggestions([]);
            return;
        }

        // otherwise, fetch suggested addresses
        const timer = setTimeout(() => {
            fetchAddressSuggestions(value);
        }, 500);

        return () => clearTimeout(timer);
    }, [value]);

    // mapbox api call
    const fetchAddressSuggestions = async (query: string) => {
        setIsLoading(true);

        try {
            const response = await fetch(`https://api.mapbox.com/geocoding/v5/mapbox.places/${encodeURIComponent(query)}.json?access_token=${MAPBOX_KEY}&autocomplete=true&types=address,poi`);
            const data = await response.json();
            if (data.features) {
                setSuggestions(data.features);
            }
        } catch (error) {
            console.error("Mapbox geocoding error: ", error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleSelect = (item: any) => {       // receive an address object
        onChangeText(item.place_name);          // update the text in the input box
        setSuggestions([]);                     // empty suggested addresses
        onAddressSelect(item);                  // send address details back to the parent page
    };

    return (
        <View className={`mb-4 ${className}`}>

            {/* return the label if any */}
            {label && <Text className='text-sm text-gray-500 mb-1'>{label}</Text>}

            <View className='flex-row border items-center border-gray-300 bg-white rounded-lg px-3 py-3'>
                <View className='w-6 items-center'>{icon}</View>

                <TextInput 
                    style={{ flex: 1, fontSize: 16, marginLeft: 10, color: 'black' }}
                    placeholder={placeholder}
                    placeholderTextColor="gray"
                    value={value}
                    onChangeText={onChangeText}
                />
                {isLoading && <ActivityIndicator size="small" color="#4DBF69" />}
            
            </View>

            {suggestions.length > 0 && (
                <View style={styles.suggestionsContainer}>
                    <FlatList
                        data={suggestions}
                        keyExtractor={(item) => item.id}
                        scrollEnabled={false}
                        renderItem={({ item }) => (
                            <TouchableOpacity
                                style={styles.suggestionsItem}
                                onPress={() => handleSelect(item)}
                            >
                                <Text style={styles.suggestionText}>{item.place_name}</Text>
                            </TouchableOpacity>
                        )}
                    />
                </View>
            )}
        </View>
    );
};


export default AddressInput

const styles = StyleSheet.create({
    suggestionsContainer: {
        backgroundColor: 'white',
        borderWidth: 1,
        borderColor: '#ddd',
        borderTopWidth: 0,
        borderBottomLeftRadius: 8,
        borderBottomRightRadius: 8,
        marginTop: -2,
        zIndex: 10,
    },
    suggestionsItem: {
        padding: 12,
        borderBottomWidth: 1,
        borderBottomColor: '#eee',
    },
    suggestionText: {
        color: '#333',
        fontSize: 14,
    },
});