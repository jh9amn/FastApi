create envirnment
> python -m venv myenv

> ls myenv/Scripts

> pip install fastapi uvicorn pydantic

run app:
> uvicorn myapp:app --reload

http://127.0.0.1:8000/docs


-----------------------------------------------------------------
-----------------------------------------------------------------

# 🧱 1. `class Patient(BaseModel)`

```python
class Patient(BaseModel):
```

* `BaseModel` comes from Pydantic 
* It helps you:

  * Validate data automatically
  * Convert JSON → Python object
  * Add constraints (like age ≥ 0)

👉 Example:

```json
{
  "name": "Aman",
  "age": 23
}
```

Pydantic ensures:

* age is an integer ✅
* no wrong data ❌

---

# 🏷️ 2. Fields with `Annotated` + `Field`

Example:

```python
id: Annotated[str, Field(description="Id of the patient")]
```

### 🔹 What is `Annotated`?

It lets you attach **extra metadata** to a type.

👉 Basic version:

```python
id: str
```

👉 Your version:

```python
id: Annotated[str, Field(...)]
```

✔ Adds:

* description
* examples
* validation rules

---

### 🔹 What is `Field()`?

Used to define:

* description (for docs)
* examples
* validation rules

Example:

```python
age: Annotated[int, Field(ge=0)]
```

👉 means:

* `age` must be **≥ 0**
* negative age ❌ not allowed

---

# 🚻 3. `Literal` (for fixed values)

```python
gender: Annotated[Literal["male", "female", "others"], ...]
```

👉 This restricts input:

Allowed:

```json
"male"
"female"
"others"
```

Not allowed:

```json
"boy" ❌
```

---

# ⚙️ 4. `@computed_field` (🔥 important)

This is a **special Pydantic feature**.

It creates fields that are:

* NOT stored
* but **calculated automatically**

---

## 📊 BMI Calculation

```python
@computed_field
@property
def bmi(self) -> float:
    bmi = round(self.weight / (self.height ** 2), 2)
    return bmi
```

👉 Formula used:

BMI = \frac{weight}{height^2}

### What it does:

* Takes `weight` and `height`
* Calculates BMI
* Rounds to 2 decimal places

👉 Example:

```python
weight = 70
height = 1.75

BMI = 22.86
```

---

## 🧾 5. `verdict` (based on BMI)

```python
@computed_field
@property
def verdict(self) -> str:
```

This uses BMI to decide health status.

### Logic:

| BMI Value | Result      |
| --------- | ----------- |
| < 18.5    | Underweight |
| 18.5–24.9 | Normal      |
| ≥ 25      | Overweight  |

---

# 🔄 Flow of Execution

When you create a patient:

```python
p = Patient(
    id="P001",
    name="Aman",
    city="Delhi",
    age=23,
    gender="male",
    height=1.75,
    weight=70
)
```

### Automatically happens:

1. ✅ Data validation
2. ✅ BMI calculated
3. ✅ Verdict generated

---

# 📦 Final Output Example

If you print:

```python
print(p.model_dump())
```

👉 Output:

```json
{
  "id": "P001",
  "name": "Aman",
  "city": "Delhi",
  "age": 23,
  "gender": "male",
  "height": 1.75,
  "weight": 70,
  "bmi": 22.86,
  "verdict": "Normal"
}
```

---

# ⚠️ Small Mistake in Your Code

```python
examples=["P)001", "P002"]
```

👉 Should be:

```python
examples=["P001", "P002"]
```

---

# 🧠 In Simple Words

Your code is:

👉 Creating a **Patient object**
👉 Validating input data
👉 Automatically calculating BMI
👉 Automatically telling if patient is healthy or not

---
