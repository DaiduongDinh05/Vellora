import { useState } from "react";
import {
  View,
  Text,
  TextInput,
  Pressable,
  KeyboardAvoidingView,
  Platform,
  Image,
} from "react-native";
import { styles } from "../styles/RegisterStyles";

export default function RegisterPage() {
  const [first, setFirst] = useState("");
  const [last, setLast] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  return (
    <KeyboardAvoidingView
      style={styles.safe}
      behavior={Platform.OS === "ios" ? "padding" : undefined}
    >
      <View style={styles.container}>
        <View style={styles.logoRow}>
          <Image
            source={require("../assets/Vellora_Dark_Logo.png")}
            style={styles.logo}
            resizeMode="contain"
          />
        </View>

        <View style={styles.fieldGroup}>
          <Text style={styles.label}>First Name</Text>
          <TextInput
            style={styles.input}
            placeholder="Enter First Name"
            placeholderTextColor="#9CA3AF"
            value={first}
            onChangeText={setFirst}
          />
        </View>

        <View style={styles.fieldGroup}>
          <Text style={styles.label}>Last Name</Text>
          <TextInput
            style={styles.input}
            placeholder="Enter Last Name"
            placeholderTextColor="#9CA3AF"
            value={last}
            onChangeText={setLast}
          />
        </View>

        <View style={styles.fieldGroup}>
          <Text style={styles.label}>Email Address</Text>
          <TextInput
            style={styles.input}
            placeholder="Enter Email"
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

        <Pressable style={styles.ctaButton}>
          <Text style={styles.ctaButtonText}>Continue</Text>
        </Pressable>

        <Text style={styles.footerText}>
          Already have an account?{" "}
          <Text style={styles.link}>Log in</Text>
        </Text>
      </View>
    </KeyboardAvoidingView>
  );
}
