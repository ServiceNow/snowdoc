/**
 * Determines if a child table extends a parent table
 * 
 * This function checks the table hierarchy to determine if the specified child table
 * is an extension of the parent table. It uses the TableUtils API to examine the
 * table relationships in the system.
 * 
 * @param {string} parent - The name of the parent table to check
 * @param {string} child - The name of the child table to verify as an extension
 * @returns {boolean} True if the child table extends the parent table, false otherwise
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