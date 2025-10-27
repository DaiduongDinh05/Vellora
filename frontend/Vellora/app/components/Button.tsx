import { ActivityIndicator, StyleSheet, Text, TouchableOpacity, TouchableOpacityProps, View } from 'react-native'
import React from 'react'

type ButtonProps = TouchableOpacityProps & {
    title: string;
    className?: string;
    isLoading?: boolean;
}

const Button: React.FC<ButtonProps> = ({
    title,
    onPress,
    className,
    isLoading = false,
    disabled = false,
    ...props
}) => {

    const toggleDisabled = disabled || isLoading;

    return (
        <TouchableOpacity
            onPress={onPress}
            disabled={toggleDisabled}
            className={`bg-accentGreen py-4 px-5 rounded-xl items-center disabled:opacity-50 ${className}`}
            {...props}
        >
            {isLoading ? (
                <ActivityIndicator color="#FFFFFF" />
            ) : (
                <Text className="text-textWhite text-base font-bold">
                    {title}
                </Text>
            )}



        </TouchableOpacity>
    )
}

export default Button
