# LL(1) Grammar Parser Project

This project is a final assignment for the *Theory of Machines and Languages* course, Spring 1404 (2025), by Mohammadjavad Jalilvand and Hossein Babazadeh. The goal is to implement a simple compiler component that parses input using LL(1) grammars and builds a parse tree using a Deterministic Pushdown Automaton (DPDA).

## 📘 Overview

We designed and implemented a simplified parsing pipeline to demonstrate how theoretical concepts from formal languages apply to real-world compiler design. The system transforms LL(1) grammars into parsing tables, builds equivalent DPDAs, and uses them to generate parse trees from input strings.

---

## 🧠 Theoretical Foundations

### 🔄 Compiler Pipeline & Parse Trees

A compiler processes source code through several stages. In this project, we focus on:

* **Lexical Analysis**: Breaking input into tokens (e.g., identifiers, numbers, symbols).
* **Syntax Analysis**: Using a grammar to build a parse tree representing the code’s structure.
* **Parse Tree**: A hierarchical representation of source code syntax based on grammar rules.

### 📜 LL(1) Grammar

* A subset of context-free grammars (CFGs) that allows deterministic parsing with 1-token lookahead.
* LL(1) grammars are free of **left-recursion** and **ambiguity**.
* A parsing table maps non-terminals and input tokens to grammar rules.

### 🤖 DPDA Construction

* We construct a **Deterministic Pushdown Automaton** (DPDA) based on the LL(1) parsing table.
* This DPDA predicts rule applications using stack operations and the current input symbol.

---

## 🛠 Implementation Phases

### 1. Grammar Input & Storage

* A class to read, store, and represent the LL(1) grammar from a file.
* Includes regular expressions for token recognition.

### 2. DPDA Representation

* A class to store and execute a DPDA.
* Processes input strings and reports acceptance/rejection.

### 3. LL(1) Grammar → DPDA Conversion

* Build a parsing table from grammar rules.
* Convert table into DPDA transitions based on stack/input combinations.

### 4. Parse Tree Generation

* Given a DPDA and input string, build a parse tree showing how the input is derived from the start symbol.
* Display the tree as text or graphically (optional).

### 5. Symbol Renaming in Parsed Text

* Given a parse tree and an input symbol (e.g., a variable name), rename it across the tree in the correct scope.
* Ensure references remain consistent.

---

## 📎 Example Grammars

### Sample 1: Arithmetic Expressions

```ebnf
E → T E'
E' → + T E' | ε
T → F T'
T' → * F T' | ε
F → (E) | IDENTIFIER | LITERAL
```

### Sample 2: Mini Language

```ebnf
Program → Function Program | ε
Function → function ID () Block
Block → { Statements }
Statements → Statement Statements | ε
Statement → ID = Expression ; | if (Expression) Block | while (Expression) Block | return Expression ;

Expression → Term Expression'
Expression' → + Term Expression' | - Term Expression' | ε
Term → Factor Term'
Term' → * Factor Term' | / Factor Term' | ε
Factor → ID | NUM | (Expression)
```

---

## 🧪 Example Input & Output

### Input (from file):

```plaintext
( a + b ) * ( c + d )
```

### Output (console or graphically):

* Display the full parse tree
* Optionally allow node selection and renaming via `id`

---

## ❓ FAQ

* **What language is recommended?**: Python is suggested for simplicity, but any language is acceptable.
* **Should we write a full C compiler?**: No. Just implement the parser with a small sample grammar.
* **Where to start?**: Begin with LL(1) grammar input → parsing table → DPDA → parse tree → rename.

---

## 🔗 Useful Links

* [LL(1) Table Construction - GeeksForGeeks](https://www.geeksforgeeks.org/construction-of-ll1-parsing-table/)
* [LL(1) Parsing Algorithm - GeeksForGeeks](https://www.geeksforgeeks.org/ll1-parsing-algorithm/)
* [LL(1) Parsing Explanation - YouTube](https://www.youtube.com/watch?v=clkHOgZUGWU)

---

## ✨ Authors

* [Hossein Babazadeh](https://www.linkedin.com/in/hossein-babazadeh-8a7754245/)
* [Mohammadjavad Jalilvand](https://www.linkedin.com/in/jalilvand-mj/)

## 👨‍🏫 Course Instructor

* [Dr. Reza Entezari Maleki](https://www.linkedin.com/in/reza-entezari-maleki-b4030b14a/)

Spring 1404 / 2025
Department of Computer Engineering
Iran University of Science and Technology


