
package org.broadinstitute.parser;
import java.util.ArrayList;
import java.util.Map;
import java.util.List;
import java.util.LinkedHashMap;
public class ParseTree implements ParseTreeNode {
  private NonTerminal nonterminal;
  private ArrayList<ParseTreeNode> children;
  private boolean isExpr, isNud, isPrefix, isInfix, isExprNud;
  private int nudMorphemeCount;
  private Terminal listSeparator;
  private String list;
  private AstTransform astTransform;
  ParseTree(NonTerminal nonterminal) {
    this.nonterminal = nonterminal;
    this.children = new ArrayList<ParseTreeNode>();
    this.astTransform = null;
    this.isExpr = false;
    this.isNud = false;
    this.isPrefix = false;
    this.isInfix = false;
    this.isExprNud = false;
    this.nudMorphemeCount = 0;
    this.listSeparator = null;
    this.list = "";
  }
  public void setExpr(boolean value) { this.isExpr = value; }
  public void setNud(boolean value) { this.isNud = value; }
  public void setPrefix(boolean value) { this.isPrefix = value; }
  public void setInfix(boolean value) { this.isInfix = value; }
  public void setExprNud(boolean value) { this.isExprNud = value; }
  public void setAstTransformation(AstTransform value) { this.astTransform = value; }
  public void setNudMorphemeCount(int value) { this.nudMorphemeCount = value; }
  public void setList(String value) { this.list = value; }
  public void setListSeparator(Terminal value) { this.listSeparator = value; }
  public int getNudMorphemeCount() { return this.nudMorphemeCount; }
  public List<ParseTreeNode> getChildren() { return this.children; }
  public boolean isInfix() { return this.isInfix; }
  public boolean isPrefix() { return this.isPrefix; }
  public boolean isExpr() { return this.isExpr; }
  public boolean isNud() { return this.isNud; }
  public boolean isExprNud() { return this.isExprNud; }
  public void add(ParseTreeNode tree) {
    if (this.children == null) {
      this.children = new ArrayList<ParseTreeNode>();
    }
    this.children.add(tree);
  }
  private boolean isCompoundNud() {
    if ( this.children.size() > 0 && this.children.get(0) instanceof ParseTree ) {
      ParseTree child = (ParseTree) this.children.get(0);
      if ( child.isNud() && !child.isPrefix() && !this.isExprNud() && !this.isInfix() ) {
        return true;
      }
    }
    return false;
  }
  public AstNode toAst() {
    if ( this.list == "slist" || this.list == "nlist" ) {
      int offset = (this.children.size() > 0 && this.children.get(0) == this.listSeparator) ? 1 : 0;
      AstList astList = new AstList();
      if ( this.children.size() == 0 ) {
        return astList;
      }
      astList.add(this.children.get(offset).toAst());
      astList.addAll((AstList) this.children.get(offset + 1).toAst());
      return astList;
    } else if ( this.list == "tlist" ) {
      AstList astList = new AstList();
      if ( this.children.size() == 0 ) {
        return astList;
      }
      astList.add(this.children.get(0).toAst());
      astList.addAll((AstList) this.children.get(2).toAst());
      return astList;
    } else if ( this.list == "mlist" ) {
      AstList astList = new AstList();
      int lastElement = this.children.size() - 1;
      if ( this.children.size() == 0 ) {
        return astList;
      }
      for (int i = 0; i < lastElement; i++) {
        astList.add(this.children.get(i).toAst());
      }
      astList.addAll((AstList) this.children.get(this.children.size() - 1).toAst());
      return astList;
    } else if ( this.isExpr ) {
      if ( this.astTransform instanceof AstTransformSubstitution ) {
        AstTransformSubstitution astSubstitution = (AstTransformSubstitution) astTransform;
        return this.children.get(astSubstitution.getIndex()).toAst();
      } else if ( this.astTransform instanceof AstTransformNodeCreator ) {
        AstTransformNodeCreator astNodeCreator = (AstTransformNodeCreator) this.astTransform;
        LinkedHashMap<String, AstNode> parameters = new LinkedHashMap<String, AstNode>();
        ParseTreeNode child;
        for ( final Map.Entry<String, Integer> parameter : astNodeCreator.getParameters().entrySet() ) {
          String name = parameter.getKey();
          int index = parameter.getValue().intValue();
          if ( index == '$' ) {
            child = this.children.get(0);
          } else if ( this.isCompoundNud() ) {
            ParseTree firstChild = (ParseTree) this.children.get(0);
            if ( index < firstChild.getNudMorphemeCount() ) {
              child = firstChild.getChildren().get(index);
            } else {
              index = index - firstChild.getNudMorphemeCount() + 1;
              child = this.children.get(index);
            }
          } else if ( this.children.size() == 1 && !(this.children.get(0) instanceof ParseTree) && !(this.children.get(0) instanceof List) ) {
            // TODO: I don't think this should ever be called
            child = this.children.get(0);
          } else {
            child = this.children.get(index);
          }
          parameters.put(name, child.toAst());
        }
        return new Ast(astNodeCreator.getName(), parameters);
      }
    } else {
      AstTransformSubstitution defaultAction = new AstTransformSubstitution(0);
      AstTransform action = this.astTransform != null ? this.astTransform : defaultAction;
      if (this.children.size() == 0) return null;
      if (action instanceof AstTransformSubstitution) {
        AstTransformSubstitution astSubstitution = (AstTransformSubstitution) action;
        return this.children.get(astSubstitution.getIndex()).toAst();
      } else if (action instanceof AstTransformNodeCreator) {
        AstTransformNodeCreator astNodeCreator = (AstTransformNodeCreator) action;
        LinkedHashMap<String, AstNode> evaluatedParameters = new LinkedHashMap<String, AstNode>();
        for ( Map.Entry<String, Integer> baseParameter : astNodeCreator.getParameters().entrySet() ) {
          String name = baseParameter.getKey();
          int index2 = baseParameter.getValue().intValue();
          evaluatedParameters.put(name, this.children.get(index2).toAst());
        }
        return new Ast(astNodeCreator.getName(), evaluatedParameters);
      }
    }
    return null;
  }
  public String toString() {
    ArrayList<String> children = new ArrayList<String>();
    for (ParseTreeNode child : this.children) {
      children.add(child.toString());
    }
    return "(" + this.nonterminal.getString() + ": " + Utility.join(children, ", ") + ")";
  }
  public String toPrettyString() {
    return toPrettyString(0);
  }
  public String toPrettyString(int indent) {
    if (this.children.size() == 0) {
      return "(" + this.nonterminal.toString() + ": )";
    }
    String spaces = Utility.getIndentString(indent);
    ArrayList<String> children = new ArrayList<String>();
    for ( ParseTreeNode node : this.children ) {
      String sub = node.toPrettyString(indent + 2).trim();
      children.add(spaces + "  " +  sub);
    }
    return spaces + "(" + this.nonterminal.toString() + ":\n" + Utility.join(children, ",\n") + "\n" + spaces + ")";
  }
}
