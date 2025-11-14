import { useState } from "react";
import {
  View,
  Text,
  TextInput,
  Pressable,
  SafeAreaView,
  KeyboardAvoidingView,
  Platform,
  Modal,
  FlatList,
} from "react-native";
import { rateStyles } from "../styles/ReimbursementStyles";
import CurrencyInput from "../components/CurrencyInput";

type AddCustomRateProps = {
  onClose?: () => void;
  onSave?: () => void;
};

type Category = {
  id: string;
  name: string;
  rate: string;
};

export default function AddCustomRatePage({ onClose, onSave }: AddCustomRateProps) {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [year, setYear] = useState("");
  const [yearPickerVisible, setYearPickerVisible] = useState(false);

  const [categories, setCategories] = useState<Category[]>([
    { id: "business", name: "Business", rate: "0.40" },
    { id: "personal", name: "Personal", rate: "0.10" },
  ]);

  const [isAddingCategory, setIsAddingCategory] = useState(false);
  const [newCategoryName, setNewCategoryName] = useState("");
  const [newCategoryRate, setNewCategoryRate] = useState("0.00");
  const [errors, setErrors] = useState("");

  const currentYear = new Date().getFullYear();
  const years = Array.from({ length: currentYear - 1999 + 2 }, (_, i) => `${2000 + i}`);

  const isDuplicateCategory = (name: string) =>
    categories.some((c) => c.name.toLowerCase() === name.toLowerCase());

  const validateBeforeSave = () => {
    if (!name.trim()) return setErrors("Name is required.");
    if (!year.trim()) return setErrors("Year is required.");
    if (categories.length === 0) return setErrors("You must add at least one category.");
    for (const c of categories) {
      if (!c.name.trim()) return setErrors("Category names cannot be empty.");
      if (!c.rate.trim()) return setErrors("Category rates cannot be empty.");
    }
    setErrors("");
    return true;
  };

  const handleSave = () => {
    if (!validateBeforeSave()) return;
    if (onSave) onSave();
  };

  const commitNewCategory = () => {
    const trimmed = newCategoryName.trim();
    if (!trimmed) {
      setIsAddingCategory(false);
      return;
    }
    if (isDuplicateCategory(trimmed)) {
      setErrors("Category already exists.");
      return;
    }

    const next: Category = {
      id: `${Date.now()}`,
      name: trimmed,
      rate: newCategoryRate || "0.00",
    };

    setCategories([...categories, next]);
    setIsAddingCategory(false);
    setNewCategoryName("");
    setNewCategoryRate("0.00");
    setErrors("");
  };

  const updateCategoryRate = (id: string, val: string) => {
    setCategories((prev) => prev.map((c) => (c.id === id ? { ...c, rate: val } : c)));
  };

  const deleteCategory = (id: string) => {
    setCategories((prev) => prev.filter((c) => c.id !== id));
  };

  return (
    <SafeAreaView style={rateStyles.safe}>
      <KeyboardAvoidingView
        style={{ flex: 1 }}
        behavior={Platform.OS === "ios" ? "padding" : undefined}
      >
        <View style={rateStyles.fullScreenWhite}>
          <View style={rateStyles.formHeaderRow}>
            <Pressable onPress={onClose} style={rateStyles.closeCircle}>
              <Text style={rateStyles.closeText}>×</Text>
            </Pressable>
            <Text style={rateStyles.formTitle}>Add custom rate</Text>
          </View>

          {errors ? (
            <Text style={{ color: "red", marginBottom: 8, fontSize: 14 }}>{errors}</Text>
          ) : null}

          <View style={rateStyles.formFieldGroup}>
            <Text style={rateStyles.formLabel}>Name</Text>
            <TextInput
              style={rateStyles.formInput}
              placeholder="Enter a name for custom rate"
              placeholderTextColor="#9CA3AF"
              value={name}
              onChangeText={setName}
            />
          </View>

          <View style={rateStyles.formFieldGroup}>
            <Text style={rateStyles.formLabel}>Description</Text>
            <TextInput
              style={rateStyles.formInput}
              placeholder="Enter a description for custom rate"
              placeholderTextColor="#9CA3AF"
              value={description}
              onChangeText={setDescription}
            />
          </View>

          <View style={rateStyles.formFieldGroup}>
            <Text style={rateStyles.formLabel}>Year</Text>
            <Pressable
              style={[rateStyles.formInput, { width: 120, justifyContent: "center" }]}
              onPress={() => setYearPickerVisible(true)}
            >
              <Text style={{ color: year ? "#000" : "#9CA3AF" }}>
                {year || "Select year"}
              </Text>
            </Pressable>
          </View>

          <Modal visible={yearPickerVisible} transparent animationType="fade">
            <View
              style={{
                flex: 1,
                backgroundColor: "rgba(0,0,0,0.4)",
                justifyContent: "center",
                alignItems: "center",
              }}
            >
              <View
                style={{
                  width: "80%",
                  backgroundColor: "white",
                  borderRadius: 16,
                  paddingVertical: 16,
                  paddingHorizontal: 12,
                }}
              >
                <Text
                  style={{
                    fontSize: 16,
                    fontWeight: "700",
                    textAlign: "center",
                    marginBottom: 12,
                  }}
                >
                  Select Year
                </Text>

                <FlatList
                  data={years}
                  keyExtractor={(item) => item}
                  style={{ maxHeight: 250 }}
                  renderItem={({ item }) => (
                    <Pressable
                      onPress={() => {
                        setYear(item);
                        setYearPickerVisible(false);
                      }}
                      style={{
                        paddingVertical: 10,
                        paddingHorizontal: 12,
                      }}
                    >
                      <Text style={{ fontSize: 16 }}>{item}</Text>
                    </Pressable>
                  )}
                />

                <Pressable
                  onPress={() => setYearPickerVisible(false)}
                  style={{
                    marginTop: 12,
                    alignSelf: "center",
                    paddingVertical: 8,
                    paddingHorizontal: 18,
                  }}
                >
                  <Text style={{ fontSize: 16, color: "#555" }}>Close</Text>
                </Pressable>
              </View>
            </View>
          </Modal>

          <View style={rateStyles.formHeadingRow}>
            <Text style={rateStyles.sectionLabel}>Categories and costs</Text>
          </View>

          {!isAddingCategory && (
            <Pressable
              onPress={() => {
                setIsAddingCategory(true);
                setErrors("");
              }}
              style={rateStyles.addRow}
            >
              <View style={rateStyles.addIconCircle}>
                <Text style={rateStyles.addIconText}>+</Text>
              </View>
              <Text style={rateStyles.addText}>Add a category</Text>
            </Pressable>
          )}

          {isAddingCategory && (
            <View>
              <View style={rateStyles.divider} />
              <View style={rateStyles.rateRow}>
                <Pressable onPress={() => setIsAddingCategory(false)}>
                  <View style={[rateStyles.minusIcon, { backgroundColor: "#555" }]} />
                </Pressable>

                <TextInput
                  style={rateStyles.categoryInput}
                  placeholder="Enter category name"
                  placeholderTextColor="#9CA3AF"
                  value={newCategoryName}
                  onChangeText={(text) => {
                    setNewCategoryName(text);
                    setErrors("");
                  }}
                  onSubmitEditing={commitNewCategory}
                  returnKeyType="done"
                />

                <CurrencyInput
                  label=""
                  value={newCategoryRate}
                  onChangeText={(text) => setNewCategoryRate(text)}
                  style={{ width: 90 }}
                />
              </View>
            </View>
          )}

          <View style={rateStyles.divider} />

          {categories.map((c, idx) => (
            <View key={c.id}>
              <View style={rateStyles.rateRow}>
                <Pressable onPress={() => deleteCategory(c.id)}>
                  <View style={rateStyles.minusIcon} />
                </Pressable>

                <Text style={rateStyles.rateRowText}>{c.name}</Text>

                <CurrencyInput
                  label=""
                  value={c.rate}
                  onChangeText={(val) => updateCategoryRate(c.id, val)}
                  style={{ width: 90 }}
                />
              </View>

              {idx < categories.length - 1 && <View style={rateStyles.divider} />}
            </View>
          ))}

          <Pressable onPress={handleSave} style={rateStyles.formSaveButton}>
            <Text style={rateStyles.formSaveText}>Save</Text>
          </Pressable>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}
