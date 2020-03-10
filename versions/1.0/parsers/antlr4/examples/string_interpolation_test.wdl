version 1.0

task foo {
  input {
    Int min_std_max_min
    String prefix
  }
  command {
    echo ${prefix}
    echo ${sep=',' min_std_max_min}
  }
}

workflow string_interpolation {

  input {
    String inp
  }

  String dquote_dollar_interp = "${inp} this is a dollar interpolation"
  String dquote_dollar_interp = "\${inp} this is a dollar interpolation"
  String dquote_tilde_interp = "~{inp} this is a tilde interpolation"
  String dquote_multi_interp = "${inp} this is a mixed interp ~{inp}"
  String dquote_only_tilde_interp = "~{inp}"
  String dquote_only_dollar_interp = "${inp}"

  String squote_dollar_interp = '${inp} this is a dollar interpolation'
  String squote_tilde_interp = '~{inp} this is a tilde interpolation'
  String squote_multi_interp = '${inp} this is a mixed interp ~{inp}'
  String squote_only_tilde_interp = '~{inp}'
  String squote_only_dollar_interp = '${inp}'


}