/**
 * Determines if the child table extends the parent table.
 * 
 * This function checks if a specified child table is an extension of a parent table
 * by using TableUtils to get the list of extensions and verifying if the child
 * table is in that list.
 * 
 * @param {String} parent - The parent table name to check
 * @param {String} child - The child table name to verify as an extension
 * @returns {Boolean} True if the child table extends the parent table, false otherwise
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