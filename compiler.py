def generate_code(text):
    import re

    # -----------------------------
    # NORMALIZATION (SAFE)
    # -----------------------------
    def normalize(line):
        line = re.sub(r"\bset\b", "let", line)
        line = re.sub(r"\bassign\b", "let", line)
        line = re.sub(r"\bmake\b", "let", line)

        line = re.sub(r"\bas\b", "be", line)

        line = re.sub(r"\bshow\b", "print", line)
        line = re.sub(r"\bdisplay\b", "print", line)

        line = re.sub(r"\bsum\b", "add", line)
        line = re.sub(r"\bplus\b", "add", line)

        return line

    lines = text.strip().split("\n")
    output = []
    variables = set()

    for line in lines:
        line = normalize(line.lower().strip())

        if not line:
            continue

        # -----------------------------
        # VARIABLE DECLARATION
        # -----------------------------
        m = re.match(r"let (\w+) (?:be|to|equal to) (\d+)", line)
        if m:
            var, val = m.groups()
            variables.add(var)
            output.append(f"{var} = {val}")
            continue

        m = re.match(r"create variable (\w+) value (\d+)", line)
        if m:
            var, val = m.groups()
            variables.add(var)
            output.append(f"{var} = {val}")
            continue

        # -----------------------------
        # INCREASE
        # -----------------------------
        m = re.match(r"increase (\w+) by (\w+)", line)
        if m:
            y, x = m.groups()

            if x not in variables or y not in variables:
                raise Exception(f"{line} → Undefined variable")

            output.append(f"{y} = {y} + {x}")
            continue

        # -----------------------------
        # ADDITION
        # -----------------------------
        m = re.match(r"add (\w+) and (\w+)", line)
        if m:
            x, y = m.groups()

            if x not in variables or y not in variables:
                raise Exception("Undefined variable")

            output.append(f"print({x} + {y})")
            continue

        # -----------------------------
        # CONDITION
        # -----------------------------
        m = re.match(r"if (\w+) (greater than|less than|equal to) (\w+) print (\w+)(?: and (\w+))?", line)
        if m:
            v1, op, v2, p1, p2 = m.groups()

            if v1 not in variables:
                raise Exception(f"{v1} not defined")

            if not v2.isdigit() and v2 not in variables:
                raise Exception(f"{v2} not defined")

            if p1 not in variables:
                raise Exception(f"{p1} not defined")

            if p2 and p2 not in variables:
                raise Exception(f"{p2} not defined")

            ops = {
                "greater than": ">",
                "less than": "<",
                "equal to": "=="
            }

            output.append(f"if {v1} {ops[op]} {v2}:")
            if p2:
                output.append(f"    print({p1}, {p2})")
            else:
                output.append(f"    print({p1})")

            continue

        # -----------------------------
        # PRINT
        # -----------------------------
        m = re.match(r"print (\w+)(?: and (\w+))?", line)
        if m:
            x, y = m.groups()

            if x not in variables:
                raise Exception(f"{x} not defined")

            if y:
                if y not in variables:
                    raise Exception(f"{y} not defined")
                output.append(f"print({x}, {y})")
            else:
                output.append(f"print({x})")

            continue

        # -----------------------------
        # LOOP
        # -----------------------------
        m = re.match(r"repeat (\d+) times (.+)", line)
        if m:
            count, command = m.groups()

            # print inside loop
            m2 = re.match(r"print (\w+)(?: and (\w+))?", command)
            if m2:
                x, y = m2.groups()

                if x not in variables:
                    raise Exception(f"{x} not defined")

                output.append(f"for _ in range({count}):")

                if y:
                    if y not in variables:
                        raise Exception(f"{y} not defined")
                    output.append(f"    print({x}, {y})")
                else:
                    output.append(f"    print({x})")

                continue

            # add inside loop
            m2 = re.match(r"add (\w+) and (\w+)", command)
            if m2:
                x, y = m2.groups()

                if x not in variables or y not in variables:
                    raise Exception("Undefined variable")

                output.append(f"for _ in range({count}):")
                output.append(f"    print({x} + {y})")
                continue

            raise Exception(f"Cannot understand inside loop: {command}")

        # -----------------------------
        # ERROR
        # -----------------------------
        raise Exception(f"Cannot understand: {line}")

    return "\n".join(output)