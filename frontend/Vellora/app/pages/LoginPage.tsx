// login.tsx – UI-only screen
import { useState } from 'react';
import { View, Text, TextInput, Pressable, KeyboardAvoidingView, Platform } from 'react-native';
import { styles } from '../styles/LoginStyles'

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  return (
    <KeyboardAvoidingView style={styles.safe} behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
      <View style={styles.container}>
        <View style={styles.logoRow}>
          <Text style={styles.logoText}>Vell</Text>
          <View style={styles.logoMark}>
            <View style={styles.logoMarkInner} />
          </View>
          <Text style={styles.logoText}>ra</Text>
        </View>

        <View style={styles.fieldGroup}>
          <Text style={styles.label}>Email Address</Text>
          <TextInput
            style={styles.input}
            placeholder="Enter Email Here"
            placeholderTextColor="#9CA3AF"
            autoCapitalize="none"
            keyboardType="email-address"
            value={email}
            onChangeText={setEmail}
          />
        </View>

        <View style={styles.fieldGroup}>
          <Text style={styles.label}>Password</Text>
          <TextInput
            style={styles.input}
            placeholder="Enter Password"
            placeholderTextColor="#9CA3AF"
            secureTextEntry
            value={password}
            onChangeText={setPassword}
          />
        </View>

        <Pressable style={({ pressed }) => [styles.cta, pressed && { opacity: 0.9 }]}>
          <Text style={styles.ctaText}>Continue</Text>
        </Pressable>

        <Text style={styles.footerText}>
          Don't have an account? <Text style={styles.link}>Sign up</Text>
        </Text>
      </View>
    </KeyboardAvoidingView>
  );
}