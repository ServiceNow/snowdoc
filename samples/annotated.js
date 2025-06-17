/**
 * @description Checks if a given child table extends a given parent table.
 * @param {string} parent The name of the potential parent table.
 * @param {string} child The name of the potential child table.
 * @returns {boolean} True if the child table extends the parent table, false otherwise.
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