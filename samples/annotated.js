/**
 * Determines if one table extends another in the ServiceNow database schema
 *
 * @function isTableExtended
 * @param {string} parent - The name of the potential parent table
 * @param {string} child - The name of the potential child table
 * @returns {boolean} True if the child table extends the parent table, false otherwise
 * @example
 * // Check if the incident table extends the task table
 * if(isTableExtended('task', 'incident')) {
 *     gs.info('Incident extends task');
 * }
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