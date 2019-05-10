import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.Statement;
import java.util.ArrayList;
import java.sql.ResultSet;
import java.sql.SQLException;


public class DBDemo {
	
	private static int returnIndex(String s) {
		if (s.equalsIgnoreCase("Imaging")) { return 1;}
		else if (s.equalsIgnoreCase("Microlensing")) { return 2;}
		else if (s.equalsIgnoreCase("RV")) { return 3;}
		else if (s.equalsIgnoreCase("Timing")) { return 4;}
		else if (s.equalsIgnoreCase("Transit")) { return 5;}
		return 6;
	}

	public static ArrayList<int[]> getExoplanetCsv() throws ClassNotFoundException {
		ArrayList<int[]> data = new ArrayList<int[]>(); 
		
		Class.forName ("com.mysql.jdbc.Driver");

		Connection conn = null;
		PreparedStatement pstmt = null;
		Statement stmt = null;
		ResultSet rs = null;
		ResultSet rs2 = null;
		try {
			conn = DriverManager.getConnection("jdbc:mysql://localhost/",
																	"root", "password");
			
			stmt = conn.createStatement();
			rs2 = stmt.executeQuery("use exoplanets");
			
			pstmt = conn.prepareStatement("select date, planetdiscmeth,"
					+ " count(*) from exoplanets group by date,"
					+ " planetdiscmeth order by date asc, planetdiscmeth asc;");
			
			rs = pstmt.executeQuery();
			
			int tempA = 0;
			int [] array = null;
			while (rs.next()) {
				int a = rs.getInt(1);
				if(a>0 && tempA != a) {
					tempA = a;
					array = new int[7];
					array[0] = a;
					data.add(array);
					
				}
				if(array!=null) {
					String b = rs.getString(2);
					int c = rs.getInt(3);
					array[returnIndex(b)] = c;
//					System.out.println (a + "\t" + b + "\t" + c);
				}
			}			
		}
		catch (SQLException e) {
			e.printStackTrace();
			int errcode = e.getErrorCode(); // possibly handle?
			String state = e.getSQLState();
			String errmsg = e.getMessage();
			System.out.println ("Error code: " + errcode);
			System.out.println ("State:      " + state);
			System.out.println ("Message:    " + errmsg);
		}
		finally {
//			System.out.println("In finally block");
			if (rs != null) {
				try {
					rs.close ();
				} catch (SQLException e) {
					e.printStackTrace();
				}
			}
			if (rs2 != null) {
				try {
					rs2.close ();
				} catch (SQLException e) {
					e.printStackTrace();
				}
			}
			
			if (stmt != null) {
				try {
					stmt.close();
				} catch (SQLException e) {
					e.printStackTrace();
				}
			}
			if (pstmt != null) {
				try {
					pstmt.close();
				} catch (SQLException e) {
					e.printStackTrace();
				}
			}			
			if (conn != null) {
				try {
					conn.close(); 
				} catch (SQLException e) {
					e.printStackTrace();
				}
			}
		}
		return data;
	}

	
	/**
	 * @param args
	 * @throws Exception 
	 */
	public static void main(String[] args) throws Exception {
		ArrayList<int[]> data = getExoplanetCsv();
		try {
//		System.out.println("Size of data: "+ data.size());
		System.out.println("Date,Imaging,Microlensing,RV,Timing,Transit,TransitTimingVariations");
		for(int i = 0; i< data.size(); i++) {
			for(int j = 0; j < 7; j++) {
				if(j != 6) {
					System.out.print(data.get(i)[j] + ", ");
				}else {System.out.print(data.get(i)[j]);}
			}
			System.out.println();
		}
		}catch(Exception e) {
			System.out.println("Exception caught: "+ e);
		}
	}

}
