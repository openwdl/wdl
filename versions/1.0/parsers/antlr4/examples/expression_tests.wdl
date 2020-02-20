version 1.0

struct Person {
    String name
    Int age
}

task exprs {

    Pair[String, String] pair = ("left", "right")
    Int i = 42
    Int j = 43
    Boolean true_ = true
    Boolean false_ = false

    command {
        echo ~{"string"}
        echo ~{("string")}
        echo ~{("left", "right").left}
        echo ~{pair.left}
        echo ~{["string"][0]}
        echo ~{true}
        echo ~{false}
        echo ~{!true}
        echo ~{true_}
        echo ~{false_}
        echo ~{!true_}
        echo ~{42}
        echo ~{-42}
        echo ~{+42}
        echo ~{i}
        echo ~{+i} # fails in Cromwell 48
        echo ~{-i} # fails in Cromwell 48
        echo ~{if true then 1 else 0}
        echo ~{if true_ then 1 else 0}
        echo ~{42 * 43}
        echo ~{i * j} # fails in Cromwell 48
        echo ~{42 / 43}
        echo ~{i / j} # fails in Cromwell 48
        echo ~{42 % 43}
        echo ~{i % j} # fails in Cromwell 48
        echo ~{42 + 43}
        echo ~{i + j} # fails in Cromwell 48
        echo ~{42 - 43}
        echo ~{i - j} # fails in Cromwell 48
        echo ~{42 < 43}
        echo ~{i < j} # fails in Cromwell 48
        echo ~{42 <= 43}
        echo ~{i <= j} # fails in Cromwell 48
        echo ~{42 > 43}
        echo ~{i > j} # fails in Cromwell 48
        echo ~{42 >= 43}
        echo ~{i >= j} # fails in Cromwell 48
        echo ~{42 == 43} # does not parse in Cromwell 48
        echo ~{i == j}
        echo ~{42 != 43}
        echo ~{i != j}
        echo ~{true && false}
        echo ~{true_ && false_}
        echo ~{true || false}
        echo ~{true_ || false_}
    }

    runtime {
        docker: "ubuntu:latest"
    }

    output {
        Array[String] lines = read_lines(stdout())
        String string = lines[0]
        String parens = lines[1]
        String left = lines[2]
        String var_left = lines[3]
        String array_element = lines[4]
        String true_ = lines[5]
        String false_ = lines[6]
        String negated = lines[7]
        String true_var = lines[8]
        String false_var = lines[9]
        String negated_var = lines[10]
        String forty_two = lines[11]
        String plus_forty_two = lines[12]
        String minus_forty_two = lines[13]
        String i = lines[14]
        String plus_i = lines[15]
        String minus_i = lines[16]
        String conditional = lines[17]
        String conditional_var = lines[18]
        String mult = lines[19]
        String mult_var = lines[20]
        String div = lines[21]
        String div_var = lines[22]
        String mod = lines[23]
        String mod_var = lines[24]
        String add = lines[25]
        String add_var = lines[26]
        String sub = lines[27]
        String sub_var = lines[28]
        String lt = lines[29]
        String lt_var = lines[30]
        String lte = lines[31]
        String lte_var = lines[32]
        String gt = lines[33]
        String gt_var = lines[34]
        String gte = lines[35]
        String gte_var = lines[36]
        String eq = lines[37]
        String eq_var = lines[38]
        String ne = lines[39]
        String ne_var = lines[40]
        String and = lines[41]
        String and_var = lines[42]
        String or = lines[43]
        String or_var = lines[44]
        # Person p = { "name": "Jamie", "age": 4 }
        # Array[Boolean] booleans = [ true, false ]
        # Array[Boolean] booleans_ = [ true_, false_ ]
    }
}

workflow commands {
    call exprs
}
