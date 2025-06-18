/**
 * Determines if a table is extended by another table
 * 
 * Checks if the specified child table extends the parent table by using TableUtils
 * to get a list of extensions and verifying if the child is in that list.
 * 
 * @param {string} parent - The parent table name to check
 * @param {string} child - The child table name to verify as an extension
 * @return {boolean} True if the child table extends the parent table, false otherwise
 */
function isTableExtended(parent, child){
    gs.include("j2js");
    var tu = new TableUtils(parent);
    if(tu.tableExists() && tu.hasExtensions()){
        var tableArrayList = tu.getTableExtensions();
        var tableArray = j2js(tableArrayList);
        if(tableArray.indexOf(child) > -1){
            return true;
        }else{
            return false;
        }
    }else{
        return false;
    }
}