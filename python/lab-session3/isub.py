##CODE REUSED FROM:
# =============================================================================
# AUSTRALIAN NATIONAL UNIVERSITY OPEN SOURCE LICENSE (ANUOS LICENSE)
# VERSION 1.3
# 
# The contents of this file are subject to the ANUOS License Version 1.3
# (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at:
# 
#   https://sourceforge.net/projects/febrl/
# 
# Software distributed under the License is distributed on an "AS IS"
# basis, WITHOUT WARRANTY OF ANY KIND, either express or implied. See
# the License for the specific language governing rights and limitations
# under the License.
# 
# The Original Software is: "stringcmp.py"
# 
# The Initial Developer of the Original Software is:
#   Dr Peter Christen (Research School of Computer Science, The Australian
#                      National University)
# 
# Copyright (C) 2002 - 2011 the Australian National University and
# others. All Rights Reserved.
# 
# Contributors:
# 
# Alternatively, the contents of this file may be used under the terms
# of the GNU General Public License Version 2 or later (the "GPL"), in
# which case the provisions of the GPL are applicable instead of those
# above. The GPL is available at the following URL: http://www.gnu.org/
# If you wish to allow use of your version of this file only under the
# terms of the GPL, and not to allow others to use your version of this
# file under the terms of the ANUOS License, indicate your decision by
# deleting the provisions above and replace them with the notice and
# other provisions required by the GPL. If you do not delete the
# provisions above, a recipient may use your version of this file under
# the terms of any one of the ANUOS License or the GPL.
# =============================================================================
#
# Freely extensible biomedical record linkage (Febrl) - Version 0.4.2
#
# See: http://datamining.anu.edu.au/linkage.html
#
# =============================================================================
"""
Comparison methods provided in this file:
  
  ontolcs        Ontology alignment string comparison based on longest common
                 substring, Hamacher product and Winkler heuristics.  
"""

# =============================================================================
import logging



def isub(str1, str2):
    return ontolcs(str1, str2)

def ontolcs(str1, str2, min_common_len = 2, common_divisor = 'average',
            min_threshold = None):
  """Return approximate string comparator measure (between 0.0 and 1.0) using
     repeated longest common substring extractions, Hamacher difference and the
     Winkler heuristic.

  USAGE:
    score = ontolcs(str1, str2, min_common_len, common_divisor, min_threshold)

  ARGUMENTS:
    str1            The first string
    str2            The second string
    min_common_len  The minimum length of a common substring
    common_divisor  Method of how to calculate the divisor, it can be set to
                    'average','shortest', or 'longest' , and is calculated
                    according to the lengths of the two input strings
    min_threshold   Minimum threshold between 0 and 1

  DESCRIPTION:
    For more information about the ontology similarity measures see:

    - Giorgos Stoilos, Giorgos Stamou and Stefanos Kollinas:
      A String Metric for Ontology Alignment
      ISWC 2005, Springer LNCS 3729, pp 624-637, 2005.
  """

  P = 0.6 # Constant for Hamacher product difference, see above mentioned paper

  if (min_common_len < 1):
    logging.exception('Minimum common length must be at least 1: %d' % \
                      (min_common_len))
    raise Exception

  if (str1 == '') or (str2 == ''):
    return 0.0
  elif (str1 == str2):
    return 1.0

  len1 = len(str1)
  len2 = len(str2)

  # Calculate the divisor - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  if (common_divisor not in ['average','shortest','longest']):
    logging.exception('Illegal value for common divisor: %s' % \
                      (common_divisor))
    raise Exception

  if (common_divisor == 'average'):
    divisor = 0.5*(len1+len2)  # Compute average string length
  elif (common_divisor == 'shortest'):
    divisor = min(len1,len2)
  else:  # Longest
    divisor = max(len1,len2)

  w_lcs =  0.0  # Basic longest common sub-string weight
  h_diff = 0.0  # Hamacher product difference

  for (s1,s2) in [(str1,str2),(str2,str1)]:

    com_str, com_len, s1, s2 = do_lcs(s1, s2)  # Find initial LCS on input

    total_com_str = com_str
    total_com_len = com_len

    while (com_len >= min_common_len): # As long as there are common substrings
      com_str, com_len, s1n, s2n = do_lcs(s1, s2)

      if (com_len >= min_common_len):
        total_com_str += com_str
        total_com_len += com_len
        s1,s2 = s1n, s2n

    w_lcs += float(total_com_len) / float(divisor)

    # Calculate Hamacher product difference for sub-strings left
    #
    s1_len = float(len(s1)) / len1
    s2_len = float(len(s2)) / len2

    h_diff += s1_len*s2_len / (P + (1-P) * (s1_len + s2_len - s1_len*s2_len))

  w_lcs /=  2.0
  h_diff /= 2.0

  assert (w_lcs >= 0.0) and (w_lcs <= 1.0), \
         'Basic LCS similarity weight outside 0-1: %f' % (w_lcs)
  assert (h_diff >= 0.0) and (h_diff <= 1.0), \
         'Hamacher product difference outside 0-1: %f' % (h_diff)

  w_lcs_wink = winklermod(str1, str2, w_lcs)

  w = w_lcs_wink - h_diff  # A weight in interval [-1,1]

  w = w/2.0 + 0.5  # Scale into [0,1]

  assert (w >= 0.0) and (w <= 1.0), \
         'Ontology LCS similarity weight outside 0-1: %f' % (w)

  # A log message - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  logging.debug('Ontology longest common substring comparator string ' + \
                '"%s" with "%s"' % (str1, str2) + ' value: %.3f' % (w))

  return w

# =============================================================================


def do_lcs(str1, str2):
  """Subroutine to extract longest common substring from the two input strings.
     Returns the common substring, its length, and the two input strings with
     the common substring removed.
  """

  n = len(str1)
  m = len(str2)

  if (n > m):  # Make sure n <= m, to use O(min(n,m)) space
    str1, str2 = str2, str1
    n, m =       m, n
    swapped = True
  else:
    swapped = False

  current = (n+1)*[0]

  com_len = 0
  com_ans1 = -1
  com_ans2 = -1

  for i in range(m):
    previous = current
    current =  (n+1)*[0]

    for j in range(n):
      if (str1[j] != str2[i]):
        current[j] = 0
      else:
        current[j] = previous[j-1]+1
        if (current[j] > com_len):
          com_len = current[j]
          com_ans1 = j
          com_ans2 = i

  com1 = str1[com_ans1-com_len+1:com_ans1+1]
  com2 = str2[com_ans2-com_len+1:com_ans2+1]

  if (com1 != com2):
    logging.exception('LCS: Different common substrings: %s / %s in ' % \
                      (com1, com2) + 'original strings: %s / %s' % \
                      (str1, str2))
    raise Exception

  # Remove common substring from input strings
  #
  str1 = str1[:com_ans1-com_len+1] + str1[1+com_ans1:]
  str2 = str2[:com_ans2-com_len+1] + str2[1+com_ans2:]

  if (swapped == True):
    return com1, com_len, str2, str1
  else:
    return com1, com_len, str1, str2

# =============================================================================

def winklermod(str1, str2, in_weight):
  """Applies the Winkler modification if beginning of strings is the same.

  USAGE:
    score = winklermod(str1, str2, in_weight)

  ARGUMENTS:
    str1       The first string
    str2       The second string
    in_weight  The basic similariy weight calculated by a string comparison
               method

  DESCRIPTION:
    As desribed in 'An Application of the Fellegi-Sunter Model of
    Record Linkage to the 1990 U.S. Decennial Census' by William E. Winkler
    and Yves Thibaudeau.

    If the begining of the two strings (up to fisrt four characters) are the
    same, the similarity weight will be increased.
 """

  # Quick check if the strings are empty or the same - - - - - - - - - - - - -
  #
  if (str1 == '') or (str2 == ''):
    return 0.0
  elif (str1 == str2):
    return 1.0

  # Compute how many characters are common at beginning - - - - - - - - - - - -
  #
  minlen = min(len(str1), len(str2))

  for same in range(1,minlen+1):
    if (str1[:same] != str2[:same]):
      break
  same -= 1
  if (same > 4):
    same = 4

  assert (same >= 0)

  winkler_weight = in_weight + same*0.1 * (1.0 - in_weight)

  assert (winkler_weight >= in_weight), 'Winkler modification is negative'

  assert (winkler_weight >= 0.0) and (winkler_weight <= 1.0), \
         'Similarity weight outside 0-1: %f' % (w)

  # A log message - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  #
  logging.debug('Winkler modification for string "%s" and "%s": Input ' % \
                (str1, str2)+'weight %.3f modified to %.3f' % \
                (in_weight, winkler_weight))

  return winkler_weight

# =============================================================================
